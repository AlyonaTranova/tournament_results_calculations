class Bowling:
    strike_symbol = 'X'
    spare_symbol = '/'
    no_symbol = '-'
    frames_quantity = 10
    strike_points = 20
    spare_points = 15
    points_quantity = 10

    class Shots:

        def __init__(self, manager):
            self.manager = manager

        def _extra_points(self, result, quantity_of_added_points=0):
            if not self.manager.extra_points:
                if quantity_of_added_points:
                    new_extra_shots_list = [quantity_of_added_points, []]
                    self.manager.extra_points.append(new_extra_shots_list)
                return
            for data_of_shots in self.manager.extra_points:
                num_extra_throws = data_of_shots[0]
                extra_shots_gathered_points = data_of_shots[1]
                if len(extra_shots_gathered_points) < num_extra_throws:
                    extra_shots_gathered_points.append(result)
            if quantity_of_added_points:
                new_extra_shots_list = [quantity_of_added_points, []]
                self.manager.extra_points.append(new_extra_shots_list)

        def data_processing(self, symbol):
            if symbol == Bowling.strike_symbol:
                return self.strike()
            elif symbol == Bowling.spare_symbol:
                return self.spare()
            elif symbol == Bowling.no_symbol:
                return self.no_symbol()
            elif '0' <= symbol <= '9':
                result = int(symbol)
                if self.manager.rules == 0:
                    return result
                elif self.manager.rules == 1:
                    self._extra_points(result)
                    return result
                else:
                    return 0
            else:
                raise ValueError(f'Ошибка: неверный символ: {symbol}')

        def strike(self):
            pass

        def spare(self):
            pass

        def no_symbol(self):
            pass

    class FirstShot(Shots):

        def strike(self):
            if self.manager.rules == 0:
                return Bowling.strike_points
            elif self.manager.rules == 1:
                result = Bowling.points_quantity
                self._extra_points(result, 2)
                return result
            else:
                return 0

        def spare(self):
            raise ValueError(f'spare ({Bowling.spare_symbol}) указан в первом броске')

        def no_symbol(self):
            return 0


    class SecondShot(Shots):
        def strike(self):
            raise ValueError(f'strike ({Bowling.strike_symbol}) указан во втором броске')

        def spare(self):
            if self.manager.rules == 0:
                return Bowling.spare_points - self.manager.spare_first_shots_points
            elif self.manager.rules == 1:
                result = Bowling.points_quantity - self.manager.spare_first_shots_points
                self._extra_points(result, 1)
                return result
            else:
                return 0

        def no_symbol(self):
            return 0

    def __init__(self, game_result, rules):
        self.game_result = game_result
        self.spare_first_shots_points = 0
        self.zero = '0'
        self.rules = rules
        self.extra_points = []

    def type_of_rules(self):
        rules = {
            0: 'National',
            1: 'International',
        }
        return rules

    def _get_extra_points_total(self):
        total = sum(sum(points[1]) for points in self.extra_points)
        return total

    def frame_processing(self):
        frames = []
        frame = ''
        if not self.game_result:
            raise ValueError(f'Вы ввели пустой результат игры.')
        if len(self.game_result) == 1 and self.game_result != Bowling.strike_symbol:
            raise ValueError('Вы ввели неправильный результат игры')
        for char_number, char in enumerate(self.game_result, start=1):
            frame += char
            if len(frame) == 1 and char_number == len(self.game_result) and char != Bowling.strike_symbol:
                raise ValueError(f'Неверный результат игры - последний фрейм: {frame}')
            if len(frame) == 2 or frame == Bowling.strike_symbol:
                if all(char.isdigit() for char in frame) and sum(int(char) for char in frame) >= 10:
                    raise ValueError(f'Неверный результат игры - неверный фрейм: ({frame})')
                frames.append(frame)
                frame = ''
        if len(frames) != Bowling.frames_quantity:
            raise ValueError('Недопустимое количество фреймов')
        else:
            return frames

    def get_score(self):
        first_shot = Bowling.FirstShot(manager=self)
        second_shot = Bowling.SecondShot(manager=self)
        total_score = 0
        frames = self.frame_processing()
        for frame in frames:
            if Bowling.spare_symbol in frame:
                self.spare_first_shots_points = int(frame.replace('/', ''))
            frame_score = 0
            for char_number, char in enumerate(frame, start=1):
                if char == Bowling.no_symbol:
                    char = self.zero
                if char_number == 1:
                    frame_score += first_shot.data_processing(char)
                else:
                    frame_score += second_shot.data_processing(char)
            total_score += frame_score
        total_score += self._get_extra_points_total()
        return {'total_score': total_score}
