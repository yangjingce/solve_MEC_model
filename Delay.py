#!/bin/python
# -*- coding:utf-8 -*-
import numpy as np


class Delay:
    def __init__(self, N_cloud, N_FAP, N_user):

        self.N_cloud = N_cloud
        self.N_FAP = N_FAP
        self.N_user = N_user
        self.N_device = self.N_cloud + self.N_FAP + self.N_user
        self.graph = np.empty([self.N_device, self.N_device])  # 延迟矩阵，D_ij:从i到j的延迟
        self.graph[:, :] = float('inf')

    def set_main_delay(self, main_delay):
        # 依据main_delay设置主要延迟
        for delay in main_delay:
            self.graph[delay[0], delay[1]] = delay[2]
        return

    def convert_direct_to_no(self):
        # 把有向图转变为无向图
        for row in range(self.N_device):
            for col in range(self.N_device):
                self.graph[row, col] = min(self.graph[row, col], self.graph[col, row])

    def dijkstra(self, startIndex, path, cost, max):  # 找单点的最短路径
        """
        求解各节点最短路径，获取path，和cost数组，
        path[i] 表示vi节点的前继节点索引，一直追溯到起点。
        cost[i] 表示vi节点的花费
        """

        v = [0] * self.N_device
        # 初始化 path，cost，V
        for i in range(self.N_device):
            if i == startIndex:
                v[startIndex] = 1
            else:
                # cost[i] = self.graph[startIndex][i]
                cost[i] = self.graph[startIndex, i]
                path[i] = (startIndex if (cost[i] < max) else -1)
        # print v, cost, path
        for i in range(1, self.N_device):
            minCost = max
            curNode = -1
            for w in range(self.N_device):
                if v[w] == 0 and cost[w] < minCost:
                    minCost = cost[w]
                    curNode = w
            # for 获取最小权值的节点
            if curNode == -1: break
            # 剩下都是不可通行的节点，跳出循环
            v[curNode] = 1
            for w in range(self.N_device):
                if v[w] == 0 and (self.graph[curNode, w] + cost[curNode] < cost[w]):
                    cost[w] = self.graph[curNode, w] + cost[curNode]  # 更新权值
                    path[w] = curNode  # 更新路径
            # for 更新其他节点的权值（距离）和路径
        return path

    def find_all_short_path(self):  # 找出所有节点的最短路径

        ans = []
        for point in range(self.N_device):
            cost = [0] * self.N_device
            path = [0] * self.N_device
            self.dijkstra(point, path, cost, float('inf'))
            ans.append(cost)
        self.graph = np.asarray(ans)
        return

    def set_between_users_un_arrive(self):
        # 把user之间的延迟设为无穷，认为之间不连接
        for user in range(-self.N_user, 0):
            for other_user in range(-self.N_user, 0):
                if user != other_user:
                    self.graph[user, other_user] = float('inf')

        return

    def get_path(self):
        return self.graph


if __name__ == '__main__':
    a = Delay(1, 3, 5)
    print(a.graph)
    a.set_main_delay(
        [(0, 1, 100), (0, 2, 100), (0, 3, 100), (1, 4, 10), (1, 5, 10), (2, 6, 10), (2, 7, 10), (3, 8, 10)])
    print(a.graph)
    a.convert_direct_to_no()
    print(a.graph)
    a.find_all_short_path()
    print(a.graph)
    a.set_between_users_un_arrive()
    print(a.graph)
