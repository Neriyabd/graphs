from collections import deque
from collections import defaultdict
from typing import Set, Dict, List
from enum import Enum

GRAPH = Dict[str, List[str]]


def dfs(graph, source):
    stack = [source]
    traversal = []
    visited = set()

    while len(stack):
        current = stack.pop()
        traversal.append(current)
        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                stack.append(neighbor)

    return traversal


graph_test = {'a': ['c', 'b'],
              'b': ['d'],
              'c': ['e', 'a'],
              'd': ['f'],
              'e': [],
              'f': []}
print(dfs(graph_test, 'a'))


def dfs_rec_helper(graph, source, visited, traversal):
    if source in visited:
        return

    visited.add(source)
    traversal.append(source)

    for neighbor in graph[source]:
        dfs_rec_helper(graph, neighbor, visited, traversal)


def dfs_rec(graph, source):
    traversal = []
    dfs_rec_helper(graph, source, set(), traversal)
    return traversal


# def dfs_rec_helper(graph, source, visited, traversal):
#     if source in visited:
#         return
#
#     visited.add(source)
#     traversal.append(source)
#
#     for neighbor in graph[source]:
#         dfs_rec_helper(graph, neighbor, visited, traversal)
#
# def dfs_rec(graph, source):
#     return dfs_rec_helper(graph, source, set(), [])
#
print(dfs_rec(graph_test, 'a'))


def bfs(graph, source):
    queue = deque([source])
    visited = set()
    traversal = []

    while queue:
        current = queue.popleft()
        visited.add(current)
        traversal.append(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append(neighbor)

    return traversal


print(bfs(graph_test, 'a'))


def has_path_helper(graph, source, dest, visited):
    if source in visited:
        return False

    if source == dest:
        return True

    visited.add(source)
    for neighbor in graph[source]:
        if has_path_helper(graph, neighbor, dest, visited):
            return True

    return False


def has_path_dfs_rec(graph, source, dest):
    return has_path_helper(graph, source, dest, visited=set())


graph_test_2 = {'a': ['c', 'b'],
                'b': [],
                'c': ['e', 'a'],
                'd': [],
                'e': ['d'],
                'f': []}

print(has_path_dfs_rec(graph_test_2, 'a', 'f'))


def has_path_bfs(graph, source, dest):
    queue = deque([source])
    visited = set()

    while queue:
        current = queue.popleft()
        if current == dest:
            return True

        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append(neighbor)

    return False


print(has_path_bfs(graph_test_2, 'a', 'd'))


def build_graph(edges):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph


edges_test = [['i', 'j'],
              ['k', 'i'],
              ['m', 'k'],
              ['k', 'l'],
              ['i', 'l']]
print(build_graph(edges_test))


def undirected_path(edges, node1, node2):
    graph = build_graph(edges)
    return has_path_dfs_rec(graph, node1, node2)


print(undirected_path(edges_test, 'i', 'l'))


def mark_components(graph: GRAPH, source: str, visited: Set[str]) -> int:
    if source in visited:
        return 0

    visited.add(source)
    for neighbor in graph[source]:
        mark_components(graph, neighbor, visited)

    return 1


def count_components(edges):
    graph = build_graph(edges)
    visited = set()
    count = 0

    for node in graph:
        count += mark_components(graph, node, visited)

    return count


print(count_components(edges_test))


def count_components(graph: GRAPH, source: str, visited: Set[str]) -> int:
    if source in visited:
        return 0

    count = 1

    visited.add(source)
    for neighbor in graph[source]:
        count += count_components(graph, neighbor, visited)

    return count


def smallest_component(edges):
    graph = build_graph(edges)
    visited = set()
    max_component = float('inf')
    for node in graph:
        if 0 < (cur_component := count_components(graph, node,
                                                  visited)) < max_component:
            print(f'cur component size = {cur_component}')
            max_component = cur_component

    return max_component


print(smallest_component(edges_test))


def shortest_path(edges, node1, node2):
    graph = build_graph(edges)
    visited = set()
    queue = deque([[node1, 0]])

    while queue:
        current, dist = queue.popleft()
        if current == node2:
            return dist

        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append([neighbor, dist + 1])

    return -1


print("shortest distance: ", end="")
print(shortest_path(edges_test, 'i', 'p'))


def new_island(area_map, source, visited, num_rows, num_cols):
    row, col = source
    legal_row = 0 <= row < num_rows
    legal_col = 0 <= col < num_cols
    if not (legal_row and legal_col):
        return 0

    if area_map[row][col] == 'W':
        return 0

    if source in visited:
        return 0

    visited.add(source)
    new_island(area_map, (row, col + 1), visited, num_rows, num_cols)
    new_island(area_map, (row, col - 1), visited, num_rows, num_cols)
    new_island(area_map, (row + 1, col), visited, num_rows, num_cols)
    new_island(area_map, (row - 1, col), visited, num_rows, num_cols)

    return 1

def islands_counter(area_map):
    visited = set()
    num_rows = len(area_map)
    num_cols = len(area_map[0])
    islands = 0
    for i in range(num_rows):
        for j in range(num_cols):
            islands += new_island(area_map, (i, j), visited, num_rows,
                                  num_cols)

    return islands

island_test = [['W', 'L', 'W', 'W', 'L', 'W'],
               ['L', 'L', 'W', 'W', 'L', 'W'],
               ['W', 'L', 'W', 'W', 'W', 'W'],
               ['W', 'W', 'W', 'L', 'L', 'W'],
               ['W', 'L', 'W', 'L', 'L', 'W'],
               ['W', 'W', 'L', 'W', 'W', 'W']]

print()
print("Number of islands")
print(islands_counter(island_test))

