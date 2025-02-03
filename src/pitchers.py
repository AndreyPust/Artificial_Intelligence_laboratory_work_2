#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Необходимо реализовать алгоритм поиска в ширину для решения
задачи о льющихся кувшинах, где цель состоит в том, чтобы
получить заданный объем воды в одном из кувшинов.
Существует набор кувшинов, каждый из которых имеет размер
(емкость) в литрах, текущий уровень воды. Задача состоит в
том, чтобы отмерить определенный объем воды. Он может оказаться
в любом из кувшинов. Состояние представлено кортежем текущих
уровней воды, а доступными действиями являются:
–	(Fill, i): наполнить i-й кувшин до самого верха
(из крана с неограниченным количеством воды);
–	(Dump, i): вылить всю воду из i-го кувшина;
–	(Pour, i, j): перелить воду из i-го кувшина в j-й кувшин,
пока либо кувшин i не опустеет, либо кувшин j не наполнится,
в зависимости от того, что наступит раньше.
"""

import math
from abc import ABC, abstractmethod
from collections import deque


class Problem(ABC):
    """
    Абстрактный класс для формальной постановки задачи.
    Новый домен (конкретная задача) должен специализировать этот класс,
    переопределяя методы actions и result, а при необходимости
    action_cost, h и is_goal.
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
        return state == self.goal

    def action_cost(self, s, a, s1):
        """Стоимость шага, по умолчанию 1."""
        return 1

    def h(self, node):
        """Эвристика, по умолчанию 0."""
        return 0


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state = state  # текущее состояние (кортеж объёмов)
        self.parent = parent  # родительский узел
        self.action = action  # действие, которое привело к этому узлу
        self.path_cost = path_cost

    def __repr__(self):
        return f"<Node {self.state}>"

    def __lt__(self, other):
        """Для приоритетных очередей."""
        return self.path_cost < other.path_cost


failure = Node("failure", path_cost=math.inf)


def expand(problem, node):
    """
    Генерируем (расширяем) дочерние узлы, применяя все действия к state.
    """

    s = node.state
    for action in problem.actions(s):
        s_next = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s_next)
        yield Node(state=s_next, parent=node, action=action, path_cost=cost)


def path_actions(node):
    """
    Восстанавливаем последовательность действий от корня до данного узла.
    """

    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    """
    Восстанавливаем последовательность состояний (кувшины) от корня до узла.
    """

    if node.parent is None:
        return [node.state]
    return path_states(node.parent) + [node.state]


def bfs(problem):
    """
    Функция алгоритма поиска в ширину.
    """

    # Создаём начальный узел
    node = Node(problem.initial)
    # Проверка: если начальное состояние уже цель
    if problem.is_goal(node.state):
        return node

    # Очередь (FIFO)
    frontier = deque([node])

    # Набор посещённых состояний
    explored = set()
    explored.add(node.state)

    # Пока очередь не пуста
    while frontier:
        current = frontier.popleft()

        # Расширяем текущий узел
        for child in expand(problem, current):
            if child.state not in explored:
                # Если это целевое состояние — возвращаем
                if problem.is_goal(child.state):
                    return child
                # Иначе помечаем как посещённое и добавляем в очередь
                explored.add(child.state)
                frontier.append(child)

    # Если очередь опустела, решения нет
    return failure


class WaterJugProblem(Problem):
    """
    Класс для задачи о льющихся кувшинах.
    Размер кувшинов - sizes
    Начальное состояние initial (кортеж),
    цель (целевой объём "goal").
    """

    def __init__(self, initial, goal, sizes):
        super().__init__(initial=initial, goal=goal)
        self.sizes = sizes  # кортеж допустимых объёмов

    def is_goal(self, state):
        """
        Цель достигается, если в одном из кувшинов есть объём == self.goal.
        """

        return any(volume == self.goal for volume in state)

    def actions(self, state):
        """
        Действия:
        (Fill, i): Наполнить i-й кувшин
        (Dump, i): Вылить i-й кувшин
        (Pour, i, j): Перелить из i-го в j-й
        """

        actions_list = []
        n = len(self.sizes)

        for i in range(n):
            (wi, si) = (state[i], self.sizes[i])

            # Fill i
            if wi < si:
                actions_list.append(("Fill", i))

            # Dump i
            if wi > 0:
                actions_list.append(("Dump", i))

            # Pour i -> j
            if wi > 0:
                for j in range(n):
                    if i != j:
                        wj, sj = state[j], self.sizes[j]
                        # Есть смысл переливать, если j не полон
                        if wj < sj:
                            actions_list.append(("Pour", i, j))

        return actions_list

    def result(self, state, action):
        """
        Применение действия к состоянию.
        """

        state = list(state)  # переводим в список для изменения
        a = action

        if a[0] == "Fill":
            i = a[1]
            state[i] = self.sizes[i]

        elif a[0] == "Dump":
            i = a[1]
            state[i] = 0

        elif a[0] == "Pour":
            i, j = a[1], a[2]
            amount_i = state[i]
            amount_j = state[j]
            capacity_j = self.sizes[j]

            # Сколько можем перелить: либо всё из i, либо пока j не наполнится
            can_pour = min(amount_i, capacity_j - amount_j)
            state[i] -= can_pour
            state[j] += can_pour

        return tuple(state)  # возвращаем неизменяемый кортеж


def main():
    """
    Главная функция программы.
    """

    initial = (0, 0, 0, 0, 0)  # начальное состояние, пусть будут пустые
    goal = 7  # целевой объем
    sizes = (5, 6, 10, 15, 20)  # размеры кувшинов

    problem = WaterJugProblem(initial, goal, sizes)
    solution_node = bfs(problem)

    if solution_node is failure:
        print("Решение не найдено!")
    else:
        # Восстановим и выведем последовательность действий
        acts = path_actions(solution_node)
        print("Последовательность действий:", acts)

        # Восстановим и выведем последовательность состояний
        state_sequence = path_states(solution_node)
        print("Последовательность состояний:", state_sequence)


if __name__ == "__main__":
    main()
