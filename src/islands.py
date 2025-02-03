#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дана бинарная матрица, где 0 представляет воду, а 1 представляет землю.
Связанные единицы формируют остров. Необходимо подсчитать общее
количество островов в данной матрице. Острова могут соединяться как по
вертикали и горизонтали, так и по диагонали.
"""

import math
from abc import ABC, abstractmethod


class Problem(ABC):
    """
    Абстрактный класс для формальной постановки задачи.
    Новый домен (конкретная задача) должен специализировать этот класс,
    переопределяя методы actions и result, а при необходимости action_cost, h и is_goal.
    """

    def __init__(self, initial=None, goal=None, **kwargs):
        self.initial = initial
        self.goal = goal
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def actions(self, state):
        """Вернуть доступные действия (операторы) из данного состояния."""
        pass

    @abstractmethod
    def result(self, state, action):
        """Вернуть результат применения действия к состоянию."""
        pass

    def is_goal(self, state):
        """Проверка, является ли состояние целевым."""
        # Для задачи «островов» конкретного целевого
        # состояния нет поэтому обычно всегда False.
        return state == self.goal

    def action_cost(self, s, a, s1):
        """
        Возвращает стоимость применения действия a,
        переводящего состояние s в состояние s1.
        По умолчанию = 1.
        """

        return 1

    def h(self, node):
        """Эвристическая функция; по умолчанию = 0."""
        return 0


class Node:
    """Узел в дереве/графе поиска."""

    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return f"<Node {self.state}>"


failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


class IslandsProblem(Problem):
    """
    Дочерний класс Problem: поиск «островов» в бинарной матрице.
    Задача: найти все клетки с 1 (земля) и считать их соединённость
    по 8 направлениям (горизонталь, вертикаль, диагональ).
    """

    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def actions(self, state):
        """
        Отдаём все соседние клетки (r2, c2), которые внутри матрицы,
        grid[r2][c2] == 1, не выходят за границы (0 <= r2 < rows, 0 <= c2 < cols).
        """

        r, c = state
        neighbors = []
        # смещения по 8 направлениям (включая диагонали)
        deltas = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for dr, dc in deltas:
            r2, c2 = r + dr, c + dc
            if 0 <= r2 < self.rows and 0 <= c2 < self.cols:
                if self.grid[r2][c2] == 1:
                    neighbors.append((r2, c2))
        return neighbors

    def result(self, state, action):
        """Переход в соседнюю клетку (action)."""
        return action


def islands_bfs(problem, start, visited):
    """
    Поиск в ширину (BFS) для обхода одного острова
    Обходит (BFS) все клетки, достижимые из 'start' (т.е. один остров).
    'visited' – множество, куда добавляем все достигнутые клетки.
    """

    from collections import deque

    frontier = deque()
    frontier.append(start)
    visited.add(start)

    while frontier:
        current = frontier.popleft()
        # Выполним расширение (expand)
        for act in problem.actions(current):
            next_state = problem.result(current, act)
            if next_state not in visited:
                visited.add(next_state)
                frontier.append(next_state)


def count_islands_bfs(grid):
    """
    Функция подсчёта количества островов.

    :param grid: Бинарная матрица
    :return: Количество островов.
    """
    problem = IslandsProblem(grid)
    visited = set()
    count_islands = 0

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                # Если это земля и мы ещё не посещали этот участок
                if (r, c) not in visited:
                    # Обходим весь остров BFS
                    islands_bfs(problem, (r, c), visited)
                    count_islands += 1

    return count_islands


def main():
    """Главная функция программы."""

    grid = [
        [1, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 1],
    ]

    number_of_islands = count_islands_bfs(grid)
    print("Общее количество островов: ", number_of_islands)


if __name__ == "__main__":
    main()
