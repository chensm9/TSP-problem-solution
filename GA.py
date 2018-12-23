import matplotlib.pyplot as plt
import math
import numpy as np
import random

class GA:
    def __init__(self, x, y):
        self.N = len(x)     # 城市数量
        self.M = 10         # 种群规模
        self.T = 1000000    # 运行代数
        self.pCorss = 0.9   # 交叉概率
        self.pMutate = 0.8  # 变异概率
        self.x = x
        self.y = y
        # 画出所有节点
        self.ax = plt.figure().add_subplot(1,1,1)
        self.ax.scatter(x, y, color='r')
        plt.pause(0.0001)
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
        self.oldPopulation = [([0] * self.N) for i in range(self.M)]    # 父代种群
        self.newPopulation = [([0] * self.N) for i in range(self.M)]    # 子代种群
        self.fitness = [0 for i in range(self.M)]  # 个体的适应度
        self.Pi = [0 for i in range(self.M)]       # 个体的累积概率
        self.lines = None
        self.display()

    # 初始化父代种群(初始子代与父代一样)
    def initGroup(self):
        # 随机打乱得到初始父代和子代
        for k in range(self.M):
            self.oldPopulation[k] = [i for i in range(self.N)]
            np.random.shuffle(self.oldPopulation[k])
            # for i in range(self.N):
            #     self.newPopulation[k][i] = self.oldPopulation[k][i]
                
    # 判断当前路径总距离作为染色体适应度
    def evaluate(self, path):
        arraylen = len(path)
        pathDist = 0
        for i in range(arraylen-1):
            pathDist += self.distance[path[i]][path[i+1]]
        pathDist += self.distance[path[arraylen-1]][path[0]]
        return pathDist

    # 计算种群中每个个体的累积概率
    def countRate(self):
        sumFitness = 0.0
        for i in self.fitness:
            sumFitness += i
        self.Pi[0] = self.fitness[0] / sumFitness
        for k in range(1, self.M):
            self.Pi[k] = self.fitness[k] / sumFitness + self.Pi[k-1]

    # 挑选适应度最高的个体
    def selectChild(self):
        # 对适应度进行排序
        for i in range(self.M-1):
            for j in range(i+1, self.M):
                if self.fitness[i] > self.fitness[j]:
                    self.fitness[i], self.fitness[j] = self.fitness[j], self.fitness[i]
                    self.oldPopulation[i], self.oldPopulation[j] = self.oldPopulation[j][:], self.oldPopulation[i][:]

        if self.fitness[0] < self.bestEvaluation:
            self.bestEvaluation = self.fitness[0]
            self.bestPath = self.oldPopulation[0][:]
            self.display()
        for k in range(math.floor(self.M/4*3)):
            self.newPopulation[k][:] = self.oldPopulation[k][:]
        for k in range(math.floor(self.M/4*3), self.M):
            ran = random.randint(0, math.floor(self.M/4*3))
            self.newPopulation[k] = self.oldPopulation[ran][:]

    # 复制染色体
    def copyGh(self, n1, n2):
        self.newPopulation[n1] = self.oldPopulation[n2][:]

    # 种群进化
    def evolution(self):
        self.selectChild()
        for k in range(0, self.M, 2):
            if random.random() < self.pCorss and k+1 < self.M:      # 交叉概率
                self.orderCrossover(k, k + 1)
            if random.random() < self.pMutate:                      # 变异概率
                self.variation(k)
            if random.random() < self.pMutate and k+1 < self.M:     # 变异概率
                self.variation(k+1)

    # 随机进行多次变异
    def variation(self, k):
        r1, r2 = random.randint(0, self.N-1), random.randint(0, self.N-1)
        while (r1 == r2):
            r2 = random.randint(0, self.N-1)
        if random.random() < 0.5:
            # 实施邻域操作  
            for i in range(math.floor((r2-r1)/2)):
                self.newPopulation[k][r1+i], self.newPopulation[k][r2-i] = self.newPopulation[k][r2-i], self.newPopulation[k][r1+i]
        else:
            self.newPopulation[k][r1], self.newPopulation[k][r2] = self.newPopulation[k][r2], self.newPopulation[k][r1]

    # 顺序交叉
    def orderCrossover(self, k1, k2):
        child1 = self.newPopulation[k1][:]
        child2 = self.newPopulation[k2][:]
        r1, r2 = random.randint(0, self.N-1), random.randint(0, self.N-1)
        while (r1 == r2):
            r2 = random.randint(0, self.N-1)
        if r1 > r2:
            r1, r2 = r2, r1
        # 生成子代交叉部分
        for i in range(self.N):
            if i >= r1 and i <= r2:
                continue
            for j in range(self.N):
                if not (self.newPopulation[k2][j] in child1):
                    child1[i] = self.newPopulation[k2][j]
                    break
            for j in range(self.N):
                if not (self.newPopulation[k1][j] in child2):
                    child2[i] = self.newPopulation[k1][j]
                    break
        self.newPopulation[k1] = child1[:]
        self.newPopulation[k2] = child2[:]

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
        plt.pause(0.00001)

    # 更新适应度
    def updateFitness(self):
        for i in range(self.M):
            self.fitness[i] = self.evaluate(self.oldPopulation[i])

    # 算法主函数
    def GArun(self):
        self.initGroup()
        self.updateFitness()
        # 计算初始化种群中各个个体的累积概率
        self.countRate()
        for t in range(self.T):
            # 进行进化
            self.evolution()
            # 将新种群newGroup复制到旧种群oldGroup中，准备下一代进化
            self.oldPopulation = self.newPopulation[:][:]
            # 更新计算种群适应度
            self.updateFitness()
            # 计算每次迭代之后种群中各个个体的累积概率
            self.countRate()
            print("t", t)
        plt.pause(100)

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