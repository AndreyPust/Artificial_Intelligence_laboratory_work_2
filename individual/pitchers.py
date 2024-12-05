#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Необходимо реализовать алгоритм поиска в ширину для решения задачи о льющихся кувшинах,
# где цель состоит в том, чтобы получить заданный объем воды в одном из кувшинов.
# Существует набор кувшинов, каждый из которых имеет размер (емкость) в литрах, текущий уровень воды.
# Задача состоит в том, чтобы отмерить определенный объем воды. Он может оказаться в любом из кувшинов.
# Состояние представлено кортежем текущих уровней воды, а доступными действиями являются:
# –	(Fill, i): наполнить i-й кувшин до самого верха (из крана с неограниченным количеством воды);
# –	(Dump, i): вылить всю воду из i-го кувшина;
# –	(Pour, i, j): перелить воду из i-го кувшина в j-й кувшин, пока либо кувшин i не опустеет,
# либо кувшин j не наполнится, в зависимости от того, что наступит раньше.


from collections import deque


def search_in_width(initial_p, goal_p, sizes_p):
    """
    Реализация алгоритма поиска в ширину для задачи о льющихся кувшинах.

    :param initial_p: начальное состояние кувшинов;
    :param goal_p: целевой объем воды;
    :param sizes_p: ёмкости кувшинов.
    :return: последовательность действий и объемы кувшинов.
    """

    # Хранение состояния и пути к нему
    queue = deque([(initial_p, [])])  # (состояние, действия)
    visited = set()
    visited.add(initial_p)

    while queue:
        state, path_p = queue.popleft()

        # Если найдено целевое состояние
        if goal_p in state:
            return path_p, state

        # Генерация всех возможных действий
        for i in range(len(sizes_p)):
            # Наполнить i-й кувшин
            new_state = list(state)
            new_state[i] = sizes_p[i]
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                queue.append((tuple(new_state), path_p + [('Fill', i)]))

            # Опустошить i-й кувшин
            new_state = list(state)
            new_state[i] = 0
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                queue.append((tuple(new_state), path_p + [('Dump', i)]))

            # Перелить из i-го в j-й
            for j in range(len(sizes_p)):
                if i != j:
                    new_state = list(state)
                    transfer = min(state[i], sizes_p[j] - state[j])
                    new_state[i] -= transfer
                    new_state[j] += transfer
                    if tuple(new_state) not in visited:
                        visited.add(tuple(new_state))
                        queue.append((tuple(new_state), path_p + [('Pour', i, j)]))

    return None, None  # Если решения нет


if __name__ == '__main__':
    initial = (0, 0, 0, 0, 0)  # начальное состояние
    goal = 7  # целевой объем
    sizes = (5, 7, 10, 15, 20)  # размеры кувшинов

    # Решение задачи
    path, final_state = search_in_width(initial, goal, sizes)

    # Вывод результатов
    if path:
        print("Решение найдено!")
        print("Действия:", path)
        print("Состояния кувшинов:", final_state)
    else:
        print("Решение невозможно.")
