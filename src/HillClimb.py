import matplotlib.pyplot as plt
import math
import numpy as np
import random

class HillClimb:
    def __init__(self, x, y):
        # 节点个数
        self.N = len(x)
        self.x = x
        self.y = y
        # 画出所有节点
        self.ax = plt.figure().add_subplot(1,1,1)
        self.ax.scatter(x, y, color='r')
        plt.pause(0.001)
        # 初始化距离矩阵 获取所有节点之间的距离
        self.distance = [([0] * self.N) for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    self.distance[i][j] = round(math.sqrt((self.x[i] - self.x[j])**2 + (self.y[i] - self.y[j])**2))
                    self.distance[j][i] = self.distance[i][j]
        # 初始化初始路径
        self.bestPath = [i for i in range(self.N)]
        np.random.shuffle(self.bestPath) # 随机打乱
        self.bestEvaluation = self.evaluate(self.bestPath)
        self.lines = None
        self.display()

    # 判断当前路径总距离
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
        plt.pause(0.0001)
        print(self.bestEvaluation, (self.bestEvaluation-26524)/26524*100)

    # 爬山算法
    def HCrun(self):
        flag = 0
        while True:
            for i in range(100):
                temp_path = [i for i in self.bestPath]
                #产生两个随机节点且ran1 < ran2
                ran1 = math.floor(random.random()*self.N)
                ran2 = math.floor(random.random()*self.N)
                while ran1 == ran2:
                    ran2 = math.floor(random.random()*self.N)
                if ran1 > ran2:
                    ran1, ran2 = ran2, ran1
                # 实施邻域操作  
                if random.random() > 0.5:
                    for i in range(math.floor((ran2-ran1)/2)):
                        temp_path[ran1+i], temp_path[ran2-i] = temp_path[ran2-i], temp_path[ran1+i]
                else:
                    temp_path[ran1], temp_path[ran2] = temp_path[ran2], temp_path[ran1]


                # 评价新值
                e = self.evaluate(temp_path)  
    
                if e < self.bestEvaluation: 
                    self.bestEvaluation = e
                    self.bestPath = temp_path
                    flag = 0
                else:
                    flag += 1
            
            self.display()
            if flag >= 100000:
                print("over")
                plt.pause(100)
                break

if __name__ == "__main__":
    N = 150
    x = []
    y = []
    # 获取所有节点的(x, y)
    for i in range(N):
        l = input().split(" ")
        if len(l) == 4:
            l.pop(0)
        print(l)
        x.append(float(l[1]))
        y.append(float(l[2]))
    hc = HillClimb(x, y)
    hc.HCrun()