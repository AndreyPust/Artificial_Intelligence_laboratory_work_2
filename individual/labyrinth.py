#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Необходимо решить задачу поиска кратчайшего пути через лабиринт, используя алгоритм поиска в ширину.
# Лабиринт представлен в виде бинарной матрицы, где 1 – это проход, а 0 – это стена.


from collections import deque


def search_in_width(maze, start, end):
    """
    Реализация поиска в ширину для нахождения кратчайшего пути в лабиринте.

    :param maze: бинарная матрица лабиринта;
    :param start: начальное положение;
    :param end: выход из лабиринта.
    :return: список клеток лабиринта кратчайшего пути и длина этого пути.
    """

    # Правила перемещения по лабиринту: вверх, вниз, влево и вправо
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    queue = deque([start])
    visited = {start: None}  # Словарь для отслеживания предков узлов

    while queue:
        current = queue.popleft()

        # Если достигли цели, строим путь
        if current == end:
            way = []
            while current is not None:
                way.append(current)
                current = visited[current]
            return way[::-1]  # возврат пути в обратном порядке

        # Проверка соседних клеток
        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < len(maze) and
                    0 <= neighbor[1] < len(maze[0]) and
                    maze[neighbor[0]][neighbor[1]] == 1 and
                    neighbor not in visited):
                visited[neighbor] = current
                queue.append(neighbor)

    return None  # Если путь не найден


if __name__ == '__main__':
    labyrinth = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    ]

    initial = (0, 0)
    goal = (11, 11)

    # Поиск кратчайшего пути в лабиринте
    path = search_in_width(labyrinth, initial, goal)

    if path:
        print("Длина пути:", len(path) - 1)
    else:
        print("Путь не найден!")
