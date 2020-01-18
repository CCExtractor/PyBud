import os
from pathlib import Path

from pybud.PyBud import PyBud
from pybud.tests.knapsack import knapsack
from pybud.tests.search_algos import *
from pybud.tests.sort_algos import *

SORT_ALGOS = [bubble_sort, merge_sort, insertion_sort, shell_sort, selection_sort]
SEARCH_ALGOS = [bfs, dfs]


def run_tests():
    debugger = PyBud()
    out_dir = Path(os.path.dirname(__file__)) / "test_logs"
    if not out_dir.is_dir():
        out_dir.mkdir()

    def output_path_gen(name):
        return out_dir / (name + ".pybud")

    def test_sorts():
        arr = [12, 11, 13, 34, 16, 7, 58, 3]
        print("\n-------------------TESTING SORTS-------------------")
        print("Unsorted list: " + str(arr))
        for algo in SORT_ALGOS:
            algo_name = algo.__name__
            print(algo_name + " result: "
                  + str(debugger.run_debug(output_path_gen(algo_name), algo, (arr,))))

    def test_searches():
        graph = {'A': ['B', 'C', 'E'],
                 'B': ['A', 'D', 'E'],
                 'C': ['A', 'F', 'G'],
                 'D': ['B'],
                 'E': ['A', 'B', 'D'],
                 'F': ['C'],
                 'G': ['C']}
        starting_vertex = 'A'
        print("\n-------------------TESTING SEARCHES-------------------")
        print("Graph: " + str(graph))
        print("Starting vertex: " + starting_vertex)
        for algo in SEARCH_ALGOS:
            algo_name = algo.__name__
            print(algo_name + " result: "
                  + str(debugger.run_debug(output_path_gen(algo_name), algo, (graph, starting_vertex))))

        val = [60, 100, 120]
        wt = [10, 20, 30]
        W = 50
        print("\n-------------------TESTING KNAPSACK-------------------")
        print("Values: " + str(val) + " Weights: " + str(wt) + " Capacity: " + str(W))
        print(knapsack.__name__ + " result: "
              + str(debugger.run_debug(output_path_gen(knapsack.__name__), knapsack, (W, wt, val))))

    test_sorts()
    test_searches()


if __name__ == '__main__':
    run_tests()
