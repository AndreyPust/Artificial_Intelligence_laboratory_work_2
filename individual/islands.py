#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Дана бинарная матрица, где 0 представляет собой воду, а 1 представляет собой землю.
# Связанные единицы по 4 стороны или по диагонали формируют остров.
# Необходимо подсчитать общее количество островов в данной матрице.


from collections import deque


def allow_move(matrix, x, y, processed):
    """
    Функция для проверки перехода в позицию следующей клетки с текущей клетки.
    Функция возвращает false, если заданы недействительные матричные координаты (выход за пределы)
    или клетка представляет воду или позиция клетки уже обработана.

    :param matrix: бинарная матрица;
    :param x: координата х потерциального перехода;
    :param y: координата y потенциального перехода;
    :param processed: обработанный узел.
    :return: разрешение на переход.
    """

    rows = len(processed)
    cols = len(processed[0])
    return (
        0 <= x < rows and
        0 <= y < cols and
        matrix[x][y] == 1 and
        not processed[x][y]
    )


def search_in_width(matrix, processed, i, j, row, col):
    """
    Реализация алгоритма поиска в ширину.

    :param matrix: бинарная матрица;
    :param processed: позиция;
    :param i: координаты x;
    :param j: координаты y;
    :param row: перемещения по x;
    :param col: перемещения по y.
    """

    # создает пустую queue и ставит в queue исходный узел
    q = deque()
    q.append((i, j))

    # пометить исходный узел как обработанный
    processed[i][j] = True

    # Цикл # до тех пор, пока queue не станет пустой
    while q:
        # удаляет передний узел из очереди и обрабатывает его
        x, y = q.popleft()

        # проверяет все восемь возможных перемещений из текущей ячейки
        # и ставить в queue каждое допустимое движение
        for k in range(len(row)):
            # пропустить, если локация недействительна, уже обработана или содержит воду
            if allow_move(matrix, x + row[k], y + col[k], processed):
                # пропустить, если местоположение неверно или уже
                # обработан или состоит из воды
                processed[x + row[k]][y + col[k]] = True
                q.append((x + row[k], y + col[k]))


def counting_islands(matrix, row, col):
    """
    Функция подсчета островов.

    :param matrix: бинарная матрица;
    :param row: перемещение по x;
    :param col: перемещение по y.
    :return: количество островов.
    """

    # Если матрица пустая
    if not matrix or not len(matrix):
        return 0

    # Расчет размерности матрицы M × N
    (M, N) = (len(matrix), len(matrix[0]))

    # запоминаем, обработана ячейка или нет
    processed = [[False for x in range(N)] for y in range(M)]

    island = 0
    for i in range(M):
        for j in range(N):
            # запускает BFS с каждого необработанного узла и увеличивает количество островов
            if matrix[i][j] == 1 and not processed[i][j]:
                search_in_width(matrix, processed, i, j, row, col)
                island = island + 1

    return island


if __name__ == '__main__':
    # Укажем, что перемещаться можно как по сторанам света, так и по смежным сторонам света
    # север, юг, запад, восток, северо-запад, северо-восток, юго-запад, юго-восток
    o_x = [-1, -1, -1, 0, 1, 0, 1, 1]
    o_y = [-1, 1, 0, -1, -1, 1, 0, 1]

    grid = [
        [1, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 1]
    ]

    print("Общее количество островов:", counting_islands(grid, o_x, o_y))
