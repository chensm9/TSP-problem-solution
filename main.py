from SA import SA
from HillClimb import HillClimb

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
    sa = SA(x, y)
    hc = HillClimb(x, y)
    sa.SA()
    hc.HillClimb()