import argparse
from rules import Bowling
from tournament import Protocol


def main():
    parser = argparse.ArgumentParser(description='Расчет результатов турнира')
    parser.add_argument('-input', type=str, help='Выберите файл c результатами игры')
    parser.add_argument('-output', type=str, help='Сохраните новый файл с расчетами')
    args = parser.parse_args('-input tournament.txt -output tour_test.txt'.split())

    try:
        result = Protocol(results_file=args.input).get_result(output_file=args.output, rules=1)
        print(result)
    except BaseException as exc:
        print(f'Ошибка расчета ({exc.__class__.__name__}): {exc.args}')


if __name__ == '__main__':
    main()
