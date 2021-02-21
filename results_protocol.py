import os.path
from rules import Bowling
from collections import defaultdict


class Protocol:

    def __init__(self, results_file, encoding='utf8'):
        self.protocol = os.path.normpath(os.path.join(os.path.dirname(__file__), results_file))
        self.encoding = encoding
        self.players_results = defaultdict(list)

    def _get_new_tour_results_dict(self):
        return {'points': {}, 'winner': None}

    def _get_tour_winner(self, tour_results):
        return sorted(tour_results.items(), key=lambda player_data: player_data[1][1], reverse=True)[0][0]

    def get_result(self, output_file, rules):
        with open(self.protocol, encoding=self.encoding) as protocol:
            protocol_results = {}
            tour_results = self._get_new_tour_results_dict()
            current_tour = None
            for row, line in enumerate(protocol, start=1):
                line = line.replace('\n', '').strip()
                if '### Tour' in line:
                    current_tour = line.replace('### Tour', '').replace('#', '').strip()
                    if not current_tour:
                        raise ValueError(f'Ошибка: неверный номер тура в строке № {row} протокола')
                    if current_tour in protocol_results:
                        raise ValueError(f'Ошибка: итоги тура № {current_tour} задублированы в протоколе')
                    tour_results = self._get_new_tour_results_dict()
                    continue
                if 'winner is' in line:
                    tour_winner = self._get_tour_winner(tour_results['points'])
                    tour_results['winner'] = tour_winner
                    protocol_results[current_tour] = tour_results
                    tour_results = None
                    current_tour = None
                    continue
                if current_tour:
                    line = line.replace('#', '')
                    player, player_game_result = line.split('\t')
                    if player in tour_results['points']:
                        raise ValueError(f'Ошибка: игрок {player} уже есть в списке')
                    tour_results['points'][player] = [player_game_result, 0]
                    try:
                        tour_results['points'][player][1] = Bowling(player_game_result, rules=rules).get_score()[
                            'total_score']
                    except BaseException as exc:
                        print(f'Ошибка при расчете очков игры в строке № {row} протокола, описание ошибки: {exc.args}')
        self.write_down_results(output_file, protocol_results)

    def write_down_results(self, output_file, protocol_results):
        result = protocol_results
        output = os.path.normpath(os.path.join(os.path.dirname(__file__), output_file))
        with open(output, mode='w', encoding='utf8') as output:
            for tour, tour_results in result.items():
                tour_header = f'Tour {tour}\n'
                output.write(tour_header)
                for player, player_result in tour_results['points'].items():
                    player_row = f'\t{player} {player_result[0]} {player_result[1]}\n'
                    output.write(player_row)
                tour_footer_row = f'\twinner is {tour_results["winner"]}\n\n'
                output.write(tour_footer_row)
