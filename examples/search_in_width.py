#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
import heapq
import math
import sys
from collections import defaultdict, deque, Counter
from itertools import combinations


class Problem:
    """
    Абстрактный класс для формальной задачи. Новый домен
    специализирует этот класс,
    переопределяя `actions` и `results`, и, возможно, другие методы.
    Эвристика по умолчанию равна 0, а стоимость действия по умолчанию
    равна 1 для всех состояний.
    Когда вы создаете экземпляр подкласса, укажите `начальное` и
    `целевое` состояния
    (или задайте метод `is_goal`) и, возможно, другие ключевые слова для
    подкласса.
    """

    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state): raise NotImplementedError

    def result(self, state, action): raise NotImplementedError

    def is_goal(self, state): return state == self.goal

    def action_cost(self, s, a, s1): return 1

    def h(self, node): return 0

    def __str__(self):
        return '{}({!r}, {!r})'.format(type(self).__name__, self.initial, self.goal)


class Node:
    """
    Узел в дереве поиска.
    """
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)

    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))

    def __lt__(self, other): return self.path_cost < other.path_cost


failure = Node('failure', path_cost=math.inf) # Алгоритм не смог найти решение.
cutoff = Node('cutoff', path_cost=math.inf) # Указывает на то, что поиск с итеративным углублением был прерван.


def expand(problem, node):
    """
    Раскрываем узел, создав дочерние узлы.
    """

    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)


def path_actions(node):
    """
    Последовательность действий, чтобы добраться до этого узла.
    """

    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    """
    Последовательность состояний, чтобы добраться до этого узла
    """

    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]


FIFOQueue = deque
LIFOQueue = list


def breadth_first_search(problem):
    """
    Функция алгоритма поиска в ширину.

    :param problem: объект формальной задачи.
    :return: решение задачи (узел) или неудачу.
    """

    node = Node(problem.initial)
    if problem.is_goal(problem.initial):
        return node
    frontier = FIFOQueue([node])
    reached = {problem.initial}
    while frontier:
        node = frontier.pop()
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return child
            if s not in reached:
                reached.add(s)
                frontier.appendleft(child)
    return failure
