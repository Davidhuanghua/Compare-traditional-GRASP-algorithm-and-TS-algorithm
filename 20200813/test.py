import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
import time
from path_relinking import solutions, GPR, Solution, calcValue
import operator


def buildSolution(data, n, m, alpha):
    value = 0


    # CREATE Solution
    solution = []
    # CREATE Contribution
    contribution = []

    best_i = random.choice([*range(n-1)])
    solution.append(best_i)

    # INITIALIZE CONTRIBUTIONS

    contribution = data[best_i]

    # SELECT THE REST OF THE ELEMENTS
    while len(solution) < m:
        best_i, largest = good(n, contribution, best_i, alpha)
        solution.append(best_i)
        value += largest

        # update contribution
        contribution += data[best_i]
        contribution[best_i] = 0

    return value, solution

def good(n, contribution, best_i, alpha):
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

def localSearch(value, solution, data, n, m):
    # initialize isinsolution
    isInSolution = [0]*n
    for i in solution:
        isInSolution[i] = 1

    improve = 1

    while improve == 1:
        improve = 0
        for i in range(m):
            # compute out_value is the total diversity of i
            try_out = solution[i]
            # compute the out_value of try_out
            out_value = 0
            for j in range(m):
                element = solution[j]
                #print(element)
                out_value += data[try_out][element]
                #print(out_value)
            # compute in_value
            move = 0
            try_in = 0
            while move == 0 and try_in <= n-1:
                # compute the in_value of try_in
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


def test(title, alpha):
    data = np.loadtxt(title, encoding='utf-8', delimiter=",")
    n = 500
    m = 40
    # when alpha = 0, please keep no repeative elements in solution
    value, solution = buildSolution(data, n, m, alpha)
    # value, solution = localSearch(value, solution, data, n, m)

    return value, solution


if __name__ == '__main__':

    title = "e.csv"
    """
    For GRASP
    """
    for alpha in [0.2, 0.5, 0.8, 0.9]:
        for time_limit in [60, 600]:
            value_all = []
            solution_all = []
            start_time = time.time()

            while time.time() - start_time <= time_limit:
                value, solution = test(title, alpha)
                value_all.append(value)
                solution_all.append(solution)

            # print(value_all, solution_all)

            if alpha == 0.2 and time_limit == 600:
                value_all = value_all.sort(reverse=True)

            print(alpha, time_limit, max(value_all))

    data = np.loadtxt(title, encoding='utf-8', delimiter=",")
    """
    For GRASP + PR
    """
    start_time = time.time()
    value_all = []
    solution_all = []
    for i in range(10):
        value, solution = test(title, 0.9)
        value_all.append(value)
        solution_all.append(solution)
        print(value, solution)
    solutionlist = solutions(value_all, solution_all)
    # 5 solutions with highest value
    solutionlist.sort(key=operator.attrgetter("value"), reverse=True)
    solutionlist = solutionlist[:5]
    best_solution = GPR(data, solutionlist)
    end_time = time.time()
    print(best_solution)
    print(best_solution.value, best_solution.solution)
    print(Solution.const)

    time_used = end_time - start_time

    print("time : ", time_used)

    value_all_GRASP = []
    solution_all_GRASP = []
    start_time_GRASP = time.time()

    while time.time() - start_time_GRASP < time_used:
       value, solution = test(title, 0.9)
       value_all_GRASP.append(value)
       solution_all_GRASP.append(solution)
    max_value = max(value_all_GRASP)
    print(max_value, solution_all_GRASP[value_all_GRASP.index(max_value)])


