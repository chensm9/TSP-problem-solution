# 对TSP问题的多种算法求解

---
## 一、局部搜索算法
采用的邻域操作：
1. 任取路径上两个点，交换其相对位置，得到一条新的路径。
2. 任取路径上两个点，对两个点之间的点进行一次翻转，得到一条新的路径。


运行结果：大致在最优解的10%~20%之间，最优情况接近5%

---
## 二、模拟退火算法
采用的邻域操作与上面局部搜索算法采取的操作相同。

相关参数：
1. 初温：1000
2. 末温：0.0001
3. 降温系数：0.99（即T[n+1] = T[n]*0.99）
4. 内循环次数：10000

运行结果：能够稳定进入最优解的10%，最优情况接近3%