import matplotlib.pyplot as plt
import math
import numpy as np
import random

class GA:
    def __init__(self, x, y):
        self.N = len(x)           # 城市数量
        self.M = 10               # 种群规模
        self.runTime = 1000000    # 运行代数
        self.pCorss = 0.9         # 交叉概率
        self.pMutate = 0.8        # 变异概率
        self.x = x
        self.y = y
        # 画出所有节点
        self.ax = plt.figure().add_subplot(1,1,1)
        self.ax.scatter(x, y, color='r')
        plt.pause(0.00001)
        # 初始化距离矩阵 获取所有节点之间的距离
        self.distance = [([0] * self.N) for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    self.distance[i][j] = round(math.sqrt((self.x[i] - self.x[j])**2 + (self.y[i] - self.y[j])**2))
                    self.distance[j][i] = self.distance[i][j]
        # 初始化随机一条路径作为最佳路径
        self.bestPath = [i for i in range(self.N)]
        np.random.shuffle(self.bestPath)
        self.bestEvaluation = self.evaluate(self.bestPath)
        self.population = []    # 种群
        self.fitness = [0 for i in range(self.M)]  # 个体的适应度
        self.Pi = [0 for i in range(self.M)]       # 个体的累积概率
        self.lines = None
        self.display()

    # 初始化种群
    def initGroup(self):
        # 随机打乱得到初始父代和子代
        for k in range(self.M):
            tempIndiv = [i for i in range(self.N)]
            np.random.shuffle(tempIndiv)
            self.population.append(tempIndiv)
                
    # 判断当前路径总距离作为染色体适应度
    def evaluate(self, path):
        arraylen = len(path)
        pathDist = 0
        for i in range(arraylen-1):
            pathDist += self.distance[path[i]][path[i+1]]
        pathDist += self.distance[path[arraylen-1]][path[0]]
        return pathDist

    # 更新图形界面
    def display(self):
        x_temp = [self.x[self.bestPath[i]] for i in range(self.N) ]
        y_temp = [self.y[self.bestPath[i]] for i in range(self.N) ]
        x_temp.append(x_temp[0])
        y_temp.append(y_temp[0])
        if self.lines != None:
            self.ax.lines.remove(self.lines[0])
        self.lines = self.ax.plot(x_temp, y_temp, color="b")
        x = str(self.bestEvaluation) + "\n" + str((round((self.bestEvaluation-26524)/26524*100, 2))) + "%"
        plt.title(x)
        plt.pause(0.000001)

    # 选择一个个体
    def getOne(self):
        r = random.randint(0, math.floor(self.M/4*3))
        return self.population[r][:]

    # 产生新的后代
    def newChild(self):
        parent1 = self.getOne()
        # 按概率交叉
        rate = random.random()
        if rate < self.pCorss:
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1
        # 按概率突变
        rate = random.random()
        if rate < self.pMutate:
            gene = self.mutation(gene)
        return gene

    # 交叉函数
    def cross(self, parent1, parent2):
        index1 = random.randint(0, self.M - 1)  # 随机生成突变起始位置 #
        index2 = random.randint(index1, self.M - 1)  # 随机生成突变终止位置 #
        tempGene = parent2[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        return newGene

    # 突变函数
    def mutation(self, gene):
        index1 = random.randint(0, self.M - 1)
        index2 = random.randint(0, self.M - 1)
        while index1 == index2:
            index2 = random.randint(0, self.M - 1)
        if index1 > index2:
            index1, index2 = index2, index1
        newGene = gene[:]
        if random.random() < 0.5:
            newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        else:
            for i in range(math.floor((index2-index1)/2)):
                newGene[index1+i], newGene[index2-i] = newGene[index2-i], newGene[index1+i]
        return newGene

    # 确定最优的个体
    def getBestIndiv(self):
        self.fitness = []
        for i in range(self.M):
            self.fitness.append(self.evaluate(self.population[i]))
        for i in range(self.M - 1):
            for j in range(i+1, self.M):
                if self.fitness[i] > self.fitness[j]:
                    self.fitness[i], self.fitness[j] = self.fitness[j], self.fitness[i]
                    self.population[i], self.population[j] = self.population[j], self.population[i]
    
    # GA算法
    def GArun(self):
        self.initGroup()
        for i in range(self.runTime):
            self.getBestIndiv()
            newPopulation = []
            # 精英原则——把最好的个体加入下一代
            newPopulation.append(self.population[0][:])
            while len(newPopulation) < self.M:
                newPopulation.append(self.newChild())
            self.population = newPopulation
            print("当前为第%d代，最优结果为：%d"%(i, self.bestEvaluation))
            if self.fitness[0] < self.bestEvaluation:
                self.bestEvaluation = self.fitness[0]
                self.bestPath = self.population[0]
                self.display()

if __name__ == "__main__":
    N = 150
    x = []
    y = []
    # 获取所有节点的(x, y)
    for i in range(N):
        l = input().split(" ")
        if len(l) == 4:
            l.pop(0)
        x.append(float(l[1]))
        y.append(float(l[2]))
    ga = GA(x, y)
    ga.GArun()