import time
import random
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
                    # print(solution == initialSolution.solution)
                    sol = Solution(solution, calcValue(data, solution))
                    # print(sol.solution == initialSolution.solution, "value", sol.value, initialSolution.value)
                    # if i == 2 and j == 3:
                    #     print("relink",i,j,sol.value, sol.solution)
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

class GRASP:
    def __init__(self):
        self.title = "e.csv"
        self.n = 500
        self.m = 40

    def buildSolution(self, data, n, m, alpha):
        value = 0

        solution_list = []
        contribution = []

        best_i = random.choice([*range(n - 1)])
        solution_list.append(best_i)
        contribution = data[best_i]

        while len(solution_list) < m:
            best_i, largest = self.good(n, contribution, best_i, alpha)
            solution_list.append(best_i)
            value += largest

            # update contribution
            contribution += data[best_i]
            contribution[best_i] = 0

        return value, solution_list

    def good(self, n, contribution, best_i, alpha):
        min = np.min(contribution)
        max = np.max(contribution)
        threshold = min + alpha * (max - min)
        RCL = []
        for i in range(n):
            if contribution[i] >= threshold:
                RCL.append(i)

        best_i = random.choice(RCL)
        largest = contribution[best_i]

        return best_i, largest

    def localSearch(self, value, solution, data, n, m):
        # initialize isinsolution
        isInSolution = [0] * n
        for i in solution:
            isInSolution[i] = 1

        improve = 1

        while improve == 1:
            improve = 0
            for i in range(m):

                try_out = solution[i]

                out_value = 0
                for j in range(m):
                    element = solution[j]
                    out_value += data[try_out][element]

                move = 0
                try_in = 0
                while move == 0 and try_in <= n - 1:
                    in_value = 0
                    if isInSolution[try_in] == 0:
                        for j in range(m):
                            element = solution[j]
                            if i != j:
                                in_value += data[try_in][element]
                    # perform the move
                    if in_value > out_value:
                        solution[i] = try_in
                        value = value - out_value + in_value
                        isInSolution[try_out] = 0
                        isInSolution[try_in] = 1
                        move = 1
                        improve = 1

                    try_in += 1

            return value, solution

    def test(self, title, alpha):
        getData = np.loadtxt(title, encoding='utf-8', delimiter=",")
        value, solution = self.buildSolution(getData, self.n, self.m, alpha)
        return value, solution

    def impleGRASP(self):

        # GRASP
        for alpha in [0.2, 0.5, 0.8, 0.9]:
            # 每一个alpha都运行50次
            for times in range(50):
                value_all = []
                solution_all = []

                value, solution = self.test(self.title, alpha)
                value_all.append(value)
                solution_all.append(solution)

            print(alpha, max(value_all))

    def plus(self):
        # For GRASP + PR
        data = np.loadtxt(self.title, encoding='utf-8', delimiter=",")
        start_time = time.time()

        value_all = []
        solution_all = []

        for i in range(10):
            value, solution = self.test(self.title, 0.9)
            value_all.append(value)
            solution_all.append(solution)

            print(value, solution)

        solutionlist = solutions(value_all, solution_all)

        solutionlist.sort(key=operator.attrgetter("value"), reverse=True)
        solutionlist = solutionlist[:5]
        best_solution = GPR(data, solutionlist)
        end_time = time.time()

        print(best_solution)
        print(best_solution.value, best_solution.solution)

        time_used = end_time - start_time

        value_all_GRASP = []
        solution_all_GRASP = []
        start_time_GRASP = time.time()

        while time.time() - start_time_GRASP < time_used:
            value, solution = self.test(self.title, 0.9)
            value_all_GRASP.append(value)
            solution_all_GRASP.append(solution)
        max_value = max(value_all_GRASP)

        print(max_value, solution_all_GRASP[value_all_GRASP.index(max_value)])


if __name__ == '__main__':
    G = GRASP()
    # G.impleGRASP()
    # 第二种方法
    G.plus()
