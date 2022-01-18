#!/bin/python
# -*- coding:utf-8 -*-
import numpy as np


class Delay:
    def __init__(self, graph, N_cloud, N_FAP, N_user):
        self.graph = graph
        self.N_cloud = N_cloud
        self.N_FAP = N_FAP
        self.N_user = N_user

    def dijkstra(self, startIndex, path, cost, max):  # 找单点的最短路径
        """
        求解各节点最短路径，获取path，和cost数组，
        path[i] 表示vi节点的前继节点索引，一直追溯到起点。
        cost[i] 表示vi节点的花费
        """
        length = len(self.graph)
        v = [0] * length
        # 初始化 path，cost，V
        for i in range(length):
            if i == startIndex:
                v[startIndex] = 1
            else:
                # cost[i] = self.graph[startIndex][i]
                cost[i] = self.graph[startIndex, i]
                path[i] = (startIndex if (cost[i] < max) else -1)
        # print v, cost, path
        for i in range(1, length):
            minCost = max
            curNode = -1
            for w in range(length):
                if v[w] == 0 and cost[w] < minCost:
                    minCost = cost[w]
                    curNode = w
            # for 获取最小权值的节点
            if curNode == -1: break
            # 剩下都是不可通行的节点，跳出循环
            v[curNode] = 1
            for w in range(length):
                if v[w] == 0 and (self.graph[curNode, w] + cost[curNode] < cost[w]):
                    cost[w] = graph[curNode, w] + cost[curNode]  # 更新权值
                    path[w] = curNode  # 更新路径
            # for 更新其他节点的权值（距离）和路径
        return path

    def find_all_short_path(self):  # 找出所有节点的最短路径
        length = len(self.graph)
        for row in range(length):
            for col in range(length):
                self.graph[row, col] = min(self.graph[row, col], self.graph[col, row])  # 把有向图转变为无向图
                # self.graph[row][ col] = min(self.graph[row][ col], self.graph[col][ row])  # 把有向图转变为无向图
        ans = []
        for point in range(length):
            cost = [0] * length
            path = [0] * length
            self.dijkstra(point, path, cost, float('inf'))
            ans.append(cost)
        self.graph = np.asarray(ans)
        return

    def set_user_un_arrive(self):
        # 把user之间的延迟设为无穷，认为之间不连接
        for user in range(-self.N_user, 0):
            for other_user in range(-self.N_user, 0):
                if user != other_user:
                    self.graph[user, other_user] = float('inf')

        return

    def get_path(self):
        return self.graph


if __name__ == '__main__':
    # max = 2147483647
    max = float('inf')
    graph = [
        [max, max, 10, max, 30, 100],
        [max, max, 5, max, max, max],
        [max, max, max, 50, max, max],
        [max, max, max, max, max, 10],
        [max, max, max, 20, max, 60],
        [max, max, max, max, max, max],
    ]
    graph = np.asarray(graph)
    a = Delay(graph, 1, 2, 3)
    a.find_all_short_path()
    a.set_user_un_arrive()
    print(a.graph)
