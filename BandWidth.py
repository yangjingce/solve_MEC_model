import numpy as np


class Bandwidth:
    """带宽类，描述了网络中设备之间的带宽"""
    def __init__(self, N_cloud, N_FAP, N_user):
        self.N_cloud = N_cloud
        self.N_FAP = N_FAP
        self.N_user = N_user
        self.N_device = self.N_cloud + self.N_FAP + self.N_user
        self.graph = np.zeros([self.N_device, self.N_device])
        """带宽矩阵，B_ij:从i到j的带宽，B_ii的带宽为None"""

    def set_main_bandwidth(self, bandwidth_list):
        """根据bandwidth_list设置主要带宽"""
        for bandwidth in bandwidth_list:
            self.graph[bandwidth[0], bandwidth[1]] = bandwidth[2]
        return

    def generate_main_bandwidth(self, cloud2FAP_bandwidth, FAP2user_bandwidth):
        """根据云到FAP的带宽和FAP到用户的带宽，生成节点间带宽，云与所有FAP相连，FAP与几个user相连,数量近似服从泊松分布"""
        # 设置云到FAP的带宽
        bandwidth_list = list()
        for cloud in range(self.N_cloud):
            for fap in range(self.N_FAP):
                bandwidth_list.append([cloud, self.N_cloud + fap, cloud2FAP_bandwidth])

        # 设置FAP到user的带宽
        p = self.N_cloud + self.N_FAP
        # 单个FAP下连的user数量近似于泊松分布
        for fap in range(self.N_cloud, self.N_cloud + self.N_FAP):
            if fap == self.N_cloud + self.N_FAP - 1:  # 如果是最后一个FAP，则剩下的user都分配给它
                one_fap_user = self.N_device
            else:
                one_fap_user = np.random.poisson((self.N_device - p)/(self.N_cloud + self.N_FAP - fap))
                one_fap_user = min(p + one_fap_user, self.N_device)
            for user in range(p, one_fap_user):
                bandwidth_list.append([fap, user, FAP2user_bandwidth])
            p = one_fap_user
            if p == self.N_device:
                break
        return bandwidth_list



    def convert_direct_to_no(self):
        """把有向图转变为无向图"""
        for row in range(self.N_device):
            for col in range(self.N_device):
                self.graph[row, col] = max(self.graph[row, col], self.graph[col, row])

    def dijkstra(self, startIndex, path, cost):  # 找单点的最短路径
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
                path[i] = (startIndex if (cost[i] != 0) else -1)
        # print v, cost, path
        for i in range(1, self.N_device):
            max_bandwidth = 0
            curNode = -1
            for w in range(self.N_device):
                if v[w] == 0 and cost[w] > max_bandwidth:
                    max_bandwidth = cost[w]
                    curNode = w
            # for 获取最大带宽的节点
            if curNode == -1: break
            # 剩下都是不可通行的节点，跳出循环
            v[curNode] = 1
            for w in range(self.N_device):
                if v[w] == 0 and (min(self.graph[w, curNode], cost[curNode]) > cost[w]):
                    cost[w] = min(self.graph[w, curNode], cost[curNode])  # 更新权值
                    path[w] = curNode  # 更新路径
            # for 更新其他节点的带宽和路径
        return path

    def find_all_bandwidth_path(self):
        """找出所有节点之间的最大带宽"""
        ans = []
        for point in range(self.N_device):
            cost = [0] * self.N_device
            path = [0] * self.N_device
            self.dijkstra(point, path, cost)
            ans.append(cost)
        self.graph = np.asarray(ans)
        return

    def set_device_self_bandwidth_None(self):
        """把device自己到自己的带宽设为None"""
        self.graph[list(range(len(self.graph))), list(range(len(self.graph)))] = None

    def get_path(self):
        return self.graph


if __name__ == '__main__':

    a = Bandwidth(1, 3, 5)
    print(a.generate_main_bandwidth(100, 10))
    # print(a.graph)
    # a.set_main_bandwidth(
    #     [(0, 1, 100), (0, 2, 100), (0, 3, 100), (1, 4, 10), (1, 5, 10), (2, 6, 10), (2, 7, 10), (3, 8, 10)])
    # print(a.graph)
    # a.convert_direct_to_no()
    # print(a.graph)
    # a.find_all_bandwidth_path()
    # print(a.graph)
    # a.set_device_self_bandwidth_None()
    # print(a.graph)