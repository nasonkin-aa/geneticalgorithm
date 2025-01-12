
import numpy as np
import random
class GeneticAlgorithm:
    def __init__(self, popsize, N, M, category, time, coefs):
        self.N = N
        self.M = M
        self.category = category
        self.time = time
        self.coefs = coefs
        self.popsize = popsize
        self.mut_chance = 1
        self.p = self.generate_random_population(self.popsize, N, M)

    @staticmethod
    def generate_random_population(popsize, N, M):
        population = []
        for _ in range(popsize):
            individual = [random.randint(0, M - 1) for _ in range(N)]# случайно генерируем особи поколичеству в популяции
            population.append(individual)
        return population
    def fitness(self, indv):
        total_time = {}
        for i in range(self.N):
            developer = indv[i]
            category = self.category[i]
            task_time = self.coefs[developer][category - 1] * self.time[i]  # Время выполнения текущей задачи

            if developer not in total_time:
                total_time[developer] = task_time

            else:
                total_time[developer] += task_time
                #print("yes"+str(total_time))

        # print(total_time)
        max_time = max(total_time.values())  # максимальное время выполнения задачи
        #print(max_time)
        return max_time

    def evaluation(self):
        fit_list = []
        for ind in self.p:
            f = self.fitness(ind)
            fit_list.append([f, ind])# добавляем в список пару (значение функции приспособленности, особь)
        fit_list.sort(key=lambda x: x[0])
        return fit_list

    def sus(self, fitness, n):

        F = np.sum(fitness)
        P = F / n
        start = np.random.randint(P)
        Pointers = [start + i * P for i in range(n)]
        Keep = []
        I = 0
        summ = fitness[I]
        for p in Pointers:
            while summ < p:
                I += 1
                summ += fitness[I]
            Keep.append(I)
            #print(Keep)
        return Keep

    def crossover(self, par1, par2):
        first = np.random.randint(N - 2)
        second = np.random.randint(first + 2, N)

        first += 1
        child1 = [*par1[:first], *par2[first:second], *par1[second:]]
        child2 = [*par2[:first], *par1[first:second], *par2[second:]]
        return child1, child2

    def mutation(self, p):
        for ind in p:
            chance = np.random.randint(100)
            if chance < self.mut_chance:
                feature_count = np.random.randint(N)
                for _ in range(feature_count):

                    ind[np.random.randint(N)] = np.random.randint(M)
        return p

    def step(self):
        best_fit = None
        for k in range(200):

            # отбор
            fit_list = self.evaluation()# список пар (значение функции приспособленности, особь)

            fits = [1000 / fit_list[i][0] for i in range(len(fit_list))]#

            n = round(self.popsize * 0.7)

            elect = self.sus(fits, n)# список индексов отобранных особей
            elected = [fit_list[i][1] for i in elect]# список отобранных особей

            # кроссовер
            next_p = []
            for _ in range(int(self.popsize / 2) - 1):
                par1 = np.random.randint(len(elected))
                par2 = np.random.randint(len(elected))
                while par2 == par1:
                    par2 = np.random.randint(len(elected))
                children = self.crossover(elected[par1], elected[par2])
                next_p.append(children[0])
                next_p.append(children[1])

            # mutation
            if best_fit == fit_list[0][0]:# если лучшее значение функции приспособленности не изменилось
                self.mut_chance += 1
            else:
                self.mut_chance = 1
            next_p = self.mutation(next_p)

            best_fit = fit_list[0][0]

            self.p = [elected[0], elected[1]] + next_p

        fit_list = self.evaluation()
        return fit_list[0]
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        N = int(file.readline().strip())#  количество задач
        category = list(map(int, file.readline().strip().split()))# категории сложности задач
        time = list(map(float, file.readline().strip().split())) # оценочное время выполнения задач
        M = int(file.readline().strip()) # количество разработчиков
        ceofs = [] # коэффициенты для разработчиков

        for i in range(M):
            coefficients = list(map(float, file.readline().strip().split()))#
            ceofs.append(coefficients)
        print("Количество задач:", N)
        print("Категории сложности задач:", category)
        print("Оценочное время выполнения задач:", time)
        print("Количество разработчиков:", M)
        print("Коэффициенты для разработчиков:")
        for coefficients in ceofs:
            print(coefficients)
        return N, category, time, M, ceofs

file_path = 'input.txt'

N, category, time, M, ceofs = read_input_file(file_path)
ga = GeneticAlgorithm(150, N, M, category, time, ceofs)

res = ga.step()
answ = [i + 1 for i in res[1]]
a = " ".join(map(str, answ))
with open('output.txt', 'w') as f:
    f.write(a)
