import operator
import numpy as np


class Solution:
    const = 0
    def __init__(self, solution, value):
        self.solution = solution
        self.value = value
        Solution.const += 1


def calcValue(data, elements):
    value = 0
    sol_len = len(elements)
    for i in range(1, sol_len):
        j = i - 1
        while j >= 0:
            value += data[elements[i]][elements[j]]
            j -= 1
    return value


def relink(data, initialSolution, guidingSolution, step):
    step_num = 0

    while step_num < step:  # truncate
        best_solution = initialSolution
        for i in initialSolution.solution:
            for j in guidingSolution.solution:
                if i != j:
                    solution = list(initialSolution.solution)
                    solution.remove(i)
                    solution.append(j)
                    sol = Solution(solution, calcValue(data, solution))

                    if sol.value > best_solution.value:
                        best_solution = sol

        initialSolution = best_solution

        step_num += 1
    return initialSolution


def GPR(data, solutionlist):
    best_solution = solutionlist[3]
    sol_num = len(solutionlist)
    for i in range(sol_num):
        # if solutionlist[i].value > best_solution.value:
            # best_solution = solutionlist[i]
        for j in range(sol_num):
            if i != j:
                # print("relink start from",i, "to", j)
                solution_new = relink(data, solutionlist[i], solutionlist[j], 20)
                # print(i,j,solution_new.value, solution_new.solution)
                if solution_new.value > best_solution.value:
                    best_solution = solution_new

    return best_solution


def solutions(value_all, solution_all):
    solutionlist = []
    for i in range(len(value_all)):
        solution = Solution(solution_all[i], value_all[i])
        solutionlist.append(solution)

    return solutionlist

