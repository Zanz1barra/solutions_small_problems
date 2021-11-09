# Я тут опять с очередной еженедельной задачей на засыпку 🙃
#
# Все вы наверное знаете, что крестики-нолики "честная игра".
# "Честной игрой" я называю игру, в которой, при оптимальной игре обоих игроков, всегда будет ничья.
#
# Задача - доказать, что "крестики нолики" честная игра 🤔
#
# P. S. Желательно доказать кодом
# Взято из сообщества канала HashCoder (https://www.youtube.com/channel/UC-fVGFZ_v29h4yKShNBDMsg)
# https://www.youtube.com/post/Ugkxwyr-FL5v1dhJtR32xtkk3T-nAclkNFIT
from typing import List

TABLE_MARKS = {
    0: ' ',
    1: 'X',
    4: 'O'
}

table = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]


def check_points(player: int, check: int) -> int:
    if check == (player * 2):
        return 100
    if check == (10 - player * 2):
        return 33
    if check == 5:
        return 0
    else:
        return 1


def count_points(player: int) -> List[List[int]]:
    result = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    check1 = table[0][0] + table[0][1] + table[0][2]
    result[0][0] += check_points(player, check1)
    result[0][1] += check_points(player, check1)
    result[0][2] += check_points(player, check1)

    check2 = table[0][0] + table[1][0] + table[2][0]
    result[0][0] += check_points(player, check2)
    result[1][0] += check_points(player, check2)
    result[2][0] += check_points(player, check2)

    check3 = table[0][0] + table[1][1] + table[2][2]
    result[0][0] += check_points(player, check3)
    result[1][1] += check_points(player, check3)
    result[2][2] += check_points(player, check3)

    check4 = table[2][0] + table[2][1] + table[2][2]
    result[2][0] += check_points(player, check4)
    result[2][1] += check_points(player, check4)
    result[2][2] += check_points(player, check4)

    check5 = table[2][0] + table[1][1] + table[0][2]
    result[2][0] += check_points(player, check5)
    result[1][1] += check_points(player, check5)
    result[0][2] += check_points(player, check5)

    check6 = table[0][1] + table[1][1] + table[2][1]
    result[0][1] += check_points(player, check6)
    result[1][1] += check_points(player, check6)
    result[2][1] += check_points(player, check6)

    check7 = table[1][0] + table[1][1] + table[1][2]
    result[1][0] += check_points(player, check7)
    result[1][1] += check_points(player, check7)
    result[1][2] += check_points(player, check7)

    check8 = table[0][2] + table[1][2] + table[2][2]
    result[0][2] += check_points(player, check8)
    result[1][2] += check_points(player, check8)
    result[2][2] += check_points(player, check8)

    for row, result_row in enumerate(result):
        for column, result_cell in enumerate(result_row):
            result[row][column] = (1 - table[row][column]) * result[row][column] - table[row][column]

    return result


def player_turn(player: int) -> bool:
    points = count_points(player)
    max_points = -1
    max_points_row = 0
    max_points_column = 0
    for row, points_row in enumerate(points):
        for column, points_cell in enumerate(points_row):
            if max_points < points_cell:
                max_points = points_cell
                max_points_row = row
                max_points_column = column
    table[max_points_row][max_points_column] = player
    return max_points > 99


def game():
    turns = 0
    player = 4
    win = False
    while (turns < 10) & (not win):
        player = 5 - player
        win = player_turn(player)
        turns += 1
    if win:
        print('Победа')
    else:
        print('Ничья')

    print(f'{TABLE_MARKS[table[0][0]]} | {TABLE_MARKS[table[0][1]]} | {TABLE_MARKS[table[0][2]]}')
    print('---------')
    print(f'{TABLE_MARKS[table[1][0]]} | {TABLE_MARKS[table[1][1]]} | {TABLE_MARKS[table[1][2]]}')
    print('---------')
    print(f'{TABLE_MARKS[table[2][0]]} | {TABLE_MARKS[table[2][1]]} | {TABLE_MARKS[table[2][2]]}')


if __name__ == '__main__':
    game()
