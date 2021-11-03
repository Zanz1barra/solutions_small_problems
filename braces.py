# Задача на засыпку
#
# 1/2/3/4/5/6/7/8/9/10 = 7
# Под '/' имеется ввиду деление
#
# Можно расставлять сколько угодно скобок, надо найти всевозможные расстановки скобок при которых равенство становится верным
# Взято из сообщества канала HashCoder (https://www.youtube.com/channel/UC-fVGFZ_v29h4yKShNBDMsg)
# https://www.youtube.com/channel/UC-fVGFZ_v29h4yKShNBDMsg/community?lb=UgkxcRjdXPTTyNDlv19TPP2NE4eRF5AhP7-k
from collections import namedtuple

FREE_FACTORS = [3, 4, 5, 6, 8, 9, 10]
ALL_FACTORS = [2, 3, 4, 5, 6, 7, 8, 9, 10]


def _calculate_numerator(choice: int) -> int:
    """
    Расчёт значения числителя на основе его битовой маски
    :param choice: битовая маска числителя
    :return: значение числителя
    """
    temp_choice = choice
    factor_index = 0
    result = 1
    while temp_choice > 0 or factor_index < len(FREE_FACTORS):
        result *= FREE_FACTORS[factor_index] ** (temp_choice % 2)
        temp_choice //= 2
        factor_index += 1
    return result


def _calculate_denominator(choice: int) -> int:
    """
    Расчёт значения знаменателя на основе битовой маски числителя
    :param choice: битовая маска числителя
    :return: значение знаменателя
    """
    temp_choice = choice ^ 0b1111111
    factor_index = 0
    result = 2
    while temp_choice > 0 or factor_index < len(FREE_FACTORS):
        result *= FREE_FACTORS[factor_index] ** (temp_choice % 2)
        temp_choice //= 2
        factor_index += 1
    return result


def _choose_factors(choice: int) -> list:
    """
    Генерация массива множителей числа на основе его битовой маски
    :param choice: битовая маска числа
    :return: список множителей числа
    """
    temp_choice = choice
    factor_index = 0
    result = [7]
    while temp_choice > 0 or factor_index < len(FREE_FACTORS):
        if temp_choice % 2 > 0:
            result.append(FREE_FACTORS[factor_index])
        temp_choice //= 2
        factor_index += 1
    return result


def find_numerator_factors() -> list:
    """
    Поиск множителей числителя путём перебора битовой маски
    :return: массив решений
    """
    result = []
    # Перебор может быть долгим, его стоит оптимизировать
    for choice in range(0b10000000):
        if _calculate_numerator(choice) == _calculate_denominator(choice):
            result.append(_choose_factors(choice) + [7])
    return result


def _rid_of_extra_braces(left: dict, right: dict) -> tuple:
    for factor in ALL_FACTORS:
        over = min(left[factor], right[factor])
        left[factor] -= over
        right[factor] -= over
    return left, right


def generate_main_placement(factors: list) -> tuple:
    """
    Генерация первичного расположения скобок
    :param factors: массив множителей числителя
    :return: left - словарь количества открывающих скобок сразу слева от числа,
            right - словарь количества закрывающих скобок сразу справа от числа
    """
    left = {}
    right = {}
    for factor in ALL_FACTORS:
        left[factor] = 0
        right[factor] = 0
        if factor in factors:
            left[factor - 1] += 1
            right[factor] += 1
    return _rid_of_extra_braces(left, right)


def generate_replacements_set(left: dict, right: dict) -> set:
    """
    Генерация множества всех вариантов расположения скобок на основе первичного расположения
    :param left: словарь количества открывающих скобок сразу слева от числа
    :param right: словарь количества закрывающих скобок сразу справа от числа
    :return: множество вариантов left (тип namedtuple) и right (тип namedtuple), тождественных первичному расположению
    """
    result = set()
    for factor in ALL_FACTORS[:-1]:
        if right[factor] > 0:
            temp_left = left.copy()
            temp_right = right.copy()
            temp_right[factor + 1] += 2 * (temp_right[factor] // 2)
            temp_right[factor] %= 2
            if temp_right[factor] == 1:
                if temp_left[factor + 1] != 1:
                    temp_right[factor + 1] += 1
                temp_left[factor] += 1
                temp_right[factor + 1] += 1
                temp_right[factor] = 0
                temp_left[factor + 1] = 0
            temp_left, temp_right = _rid_of_extra_braces(temp_left, temp_right)
            result.update(generate_replacements_set(temp_left, temp_right))
    left_tuple = tuple([left[factor] for factor in ALL_FACTORS])
    right_tuple = tuple([right[factor] for factor in ALL_FACTORS])
    result.add((left_tuple, right_tuple))
    return result


def print_replacements(replacements: set) -> int:
    """
    Вывод в консоль всех вариантов расположения скобок
    :param replacements: множество всех вариантов расположения скобок
    :return: количество вариантов расположения скобок
    """
    for left, right in replacements:
        if isinstance(left, dict) & isinstance(right, dict):
            output_string = '1/'
            for factor in ALL_FACTORS:
                output_string += ('(' * left[factor])
                output_string += str(factor)
                output_string += (')' * right[factor])
                if factor != ALL_FACTORS[-1]:
                    output_string += '/'
            print(output_string)
        elif isinstance(left, tuple) & isinstance(right, tuple):
            output_string = '1/'
            for number, factor in enumerate(ALL_FACTORS):
                output_string += ('(' * left[number])
                output_string += str(factor)
                output_string += (')' * right[number])
                if factor != ALL_FACTORS[-1]:
                    output_string += '/'
            print(output_string)
        else:
            print("Wrong inputs")
    return len(replacements)


if __name__ == '__main__':
    number_solutions = 0
    for solution in find_numerator_factors():
        left_braces, right_braces = generate_main_placement(solution)
        variations_set = generate_replacements_set(left_braces, right_braces)
        number_solutions += print_replacements(variations_set)
    print(f'Find {number_solutions} solutions')
