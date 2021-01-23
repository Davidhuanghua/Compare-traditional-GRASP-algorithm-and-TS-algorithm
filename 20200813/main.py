import time
import random
import operator
import numpy as np


def linkpath(data, initiating_solution, guiding_solution, phase):
    phase_number = 0

    while phase_number < phase:
        best_solution = initiating_solution
        for x in initiating_solution.solution:
            for y in guiding_solution.solution:
                if x != y:
                    sol_list = list(initiating_solution.solution)
                    sol_list.remove(x)
                    sol_list.append(y)

                    solution_list = Distance(sol_list, diversitydistance(data, sol_list))

                    if solution_list.value > best_solution.value:
                        best_solution = solution_list

        initiating_solution = best_solution

        phase_number += 1
    return initiating_solution


def diversitydistance(data, E):
    distance = 0

    for x in range(1, len(E)):
        y = x - 1
        while y >= 0:
            distance += data[E[x]][E[y]]
            y = y - 1
    return distance


def Sols(total_distance, total_solution):
    distance_list = []

    for case in range(len(total_distance)):
        sol = Distance(total_solution[case], total_distance[case])
        distance_list.append(sol)

    return distance_list


def path_relinking(value, distance_list):
    most_diversity = distance_list[0]
    for x in range(len(distance_list)):
        for y in range(len(distance_list)):
            if x == y:
                pass
            else:
                updatedDistance = linkpath(value, distance_list[x], distance_list[y], 20)
                if updatedDistance.value <= most_diversity.value:
                    pass
                else:
                    most_diversity = updatedDistance

    return most_diversity


class pureGRASP:
    def __init__(self):
        self.title = "e.csv"
        self.m = 40
        self.n = 500

    def Construction(self, alpha, data,  m, n):
        value = 0

        # contribution = []
        distance_list = []

        best_case = random.choice([*range(n - 1)])
        distance_list.append(best_case)
        Contrib = data[best_case]

        try:
            while len(distance_list) < m:
                best_case, mostDiversity = self.highQuality(n, Contrib, best_case, alpha)
                distance_list.append(best_case)
                value = value + mostDiversity

                Contrib = Contrib + data[best_case]
                Contrib[best_case] = 0
        except Exception as e:
            print(e)

        return value, distance_list

    def highQuality(self, n, Contrib, best_case, alpha):
        min_distance = np.min(Contrib)
        max_distance = np.max(Contrib)
        threshold = min_distance + alpha * (max_distance - min_distance)

        RCL = []

        for x in range(n):
            if Contrib[x] < threshold:
                pass
            else:
                RCL.append(x)

        best_case = random.choice(RCL)
        mostDiversity = Contrib[best_case]

        return best_case, mostDiversity

    # def distance_list(self, value, solution, data, n, m):
    #
    #     isInSolution = n * [0]
    #
    #     for x in solution:
    #         isInSolution[x] = 1
    #
    #     better = 1
    #
    #     while better == 1:
    #         better = 0
    #         for x in range(m):
    #             try_out = solution[x]
    #
    #             out_value = 0
    #
    #             for y in range(m):
    #                 element = solution[y]
    #                 out_value += data[try_out][element]
    #
    #             move = 0
    #             try_in = 0
    #             while move == 0 and try_in <= n - 1:
    #                 in_value = 0
    #                 if isInSolution[try_in] == 0:
    #                     for j in range(m):
    #                         element = solution[j]
    #                         if x != j:
    #                             in_value = in_value + data[try_in][element]
    #
    #                 if in_value > out_value:
    #                     solution[x] = try_in
    #                     value = value - out_value + in_value
    #                     isInSolution[try_out] = 0
    #                     isInSolution[try_in] = 1
    #                     move = 1
    #                     better = 1
    #
    #                 try_in += 1
    #
    #         return value, solution

    def do(self, title, alpha):
        loding = np.loadtxt(title, encoding='utf-8', delimiter=",")
        diversity, distance = self.Construction(alpha, loding, self.m, self.n)
        return diversity, distance

    def pure_GRASP(self):
        try:
            # pureGRASP
            for alpha in [0.2, 0.5, 0.8, 0.9]:
                # 每一个alpha都运行50次
                for times in range(50):
                    totalDiversity = []
                    totalDistance = []
                    diversity, distance = self.do(self.title, alpha)
                    totalDistance.append(distance)
                    totalDiversity.append(diversity)

                print('\n When the value of the alpha is %s,\n The max value of the totalDiversity is %s' % (
                    alpha, max(totalDiversity)))

        except Exception as e:
            print(e)

    def grasp_pr(self):
        loading = np.loadtxt(self.title, encoding='utf-8', delimiter=",")
        totalDiversity = []
        totalDistance = []

        for case in range(1, 11):
            diversity, distance = self.do(self.title, 0.9)
            totalDistance.append(distance)
            totalDiversity.append(diversity)

            print('(NO.%d)The result of value: %s\nThe result of solution: %s\n' % (case, diversity, distance))

        soul_list = Sols(totalDiversity, totalDistance)

        soul_list.sort(key=operator.attrgetter("value"), reverse=True)
        soul_list = soul_list[:5]
        best_solution = path_relinking(loading, soul_list)

        print(' best value:%s\n best solution:%s' % (best_solution.value, best_solution.solution))

        GRASP_diversity = []
        GRASP_distance = []
        times = 1
        while times <= 50:
            diversity, distance = self.do(self.title, 0.9)
            GRASP_diversity.append(diversity)
            GRASP_distance.append(distance)

            times += 1

        max_diversity = max(GRASP_diversity)

        print('\n\n\nGet the maximum value:%s\nThe all max solution:%s\n' % (
            max_diversity, GRASP_distance[GRASP_diversity.index(max_diversity)]))


class Distance:
    num = 0

    def __init__(self, distance, diversity):
        self.solution = distance
        self.value = diversity
        Distance.num = Distance.num + 1


if __name__ == '__main__':
    try:
        G = pureGRASP()
        # case one
        G.pure_GRASP()
        # case two
        # G.grasp_pr()
    except Exception as e:
        print(e)

    finally:
        print('End of the program')
