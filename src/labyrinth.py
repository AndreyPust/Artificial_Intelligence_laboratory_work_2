#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Необходимо решить задачу поиска кратчайшего пути через лабиринт,
используя алгоритм поиска в ширину. Лабиринт представлен в виде
бинарной матрицы, где 1 – это проход, а 0 – это стена.
"""

from abc import ABC, abstractmethod
from collections import deque


class Problem(ABC):
    """
    Абстрактный класс для формальной постановки задачи.
    Новый домен (конкретная задача) должен специализировать этот класс,
    переопределяя методы actions и result, а при необходимости
    action_cost, h и is_goal.
    """

    def __init__(self, initial=None, goal=None):
        self.initial = initial
        self.goal = goal

    @abstractmethod
    def actions(self, state):
        """Вернуть доступные действия (операторы) из данного состояния."""
        pass

    @abstractmethod
    def result(self, state, action):
        """Вернуть результат применения действия к состоянию."""
        pass

    def is_goal(self, state):
        """Определить, достигнуто ли целевое состояние."""
        return state == self.goal


class LabyrinthProblem(Problem):
    """
    Лабиринт задан бинарной матрицей:
    1 - проход,
    0 - стена.
    Нужно найти путь от initial до goal.
    """

    def __init__(self, labyrinth, initial, goal):
        super().__init__(initial=initial, goal=goal)
        self.labyrinth = labyrinth
        self.rows = len(labyrinth)
        self.cols = len(labyrinth[0]) if labyrinth else 0

    def actions(self, state):
        """Список смежных координат, куда можно перейти по четырём направлениям (если там 1)."""
        (r, c) = state
        moves = []
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.labyrinth[nr][nc] == 1:
                    moves.append((nr, nc))
        return moves

    def result(self, state, action):
        """Переход в соседнюю клетку."""
        return action


def bfs_labyrinth(problem):
    """
    Ищет кратчайший путь (по числу шагов) от problem.initial до problem.goal
    с помощью алгоритма поиска в ширину (BFS).
    Возвращает длину пути или None, если путь не найден.
    """

    start = problem.initial
    goal = problem.goal

    # Если начальное состояние совпадает с целевым
    if start == goal:
        return 0

    queue = deque([(start, 0)])

    # Посещенные состояния
    visited = set()
    visited.add(start)

    while queue:
        (current, dist) = queue.popleft()

        for action in problem.actions(current):
            next_state = problem.result(current, action)
            if next_state not in visited:
                visited.add(next_state)
                # Проверяем, не является ли новая клетка целевым состоянием
                if problem.is_goal(next_state):
                    return dist + 1
                # Если нет, добавляем в очередь с расстоянием dist+1
                queue.append((next_state, dist + 1))

    # Если очередь опустела и целевое состояние не достигнуто — пути нет
    return None


def main():
    """
    Главная функция программы.
    """
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
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    ]

    initial = (0, 0)
    goal = (11, 11)

    problem = LabyrinthProblem(labyrinth, initial, goal)
    distance = bfs_labyrinth(problem)

    if distance is None:
        print("Путь не найден.")
    else:
        print("Длина пути: ", distance)


if __name__ == "__main__":
    main()
