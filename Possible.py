import numpy as np


class Possible:
    def __init__(self, N_cloud, N_FAP, N_user, N_task):
        self.N_cloud = N_cloud
        self.N_FAP = N_FAP
        self.N_user = N_user
        self.N_device = self.N_cloud + self.N_FAP + self.N_user
        self.N_task = N_task
        self.P = np.zeros([self.N_device, self.N_task])  # 概率矩阵，P_ur:u用户提出r任务的概率

    def zipf(self, alpha):  # 生成zipf概率质量函数
        u = sum([pow(i, -alpha) for i in range(1, self.N_task + 1)])
        temp = np.zeros([self.N_task])
        # temp = [0 for i in range(self.N_task)]
        for i in range(1, self.N_task + 1):
            temp[i - 1] = pow(i, -alpha) / u
        return temp

    def set_possible_zipf(self, alpha):  # 生成随机的zipf概率矩阵
        zipf_possible = self.zipf(alpha)
        index = np.array(range(self.N_task))
        for device in range(self.N_cloud + self.N_FAP, self.N_device):
            temp_index = np.random.permutation(index)
            for i in range(self.N_task):
                self.P[device, temp_index[i]] = zipf_possible[i]
        return

    def set_certain_zipf(self):  # 生成确定的zipf概率矩阵
        self.P = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                           [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                           [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                           [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                           [0.05690286, 0.04877388, 0.11380572, 0.04267714, 0.03793524, 0.03414172, 0.34141715,
                            0.08535429, 0.17070858, 0.06828343],
                           [0.17070858, 0.04877388, 0.34141715, 0.06828343, 0.03414172, 0.05690286, 0.11380572,
                            0.03793524, 0.04267714, 0.08535429],
                           [0.34141715, 0.11380572, 0.06828343, 0.03414172, 0.04877388, 0.17070858, 0.08535429,
                            0.05690286, 0.04267714, 0.03793524],
                           [0.03414172, 0.04267714, 0.03793524, 0.04877388, 0.05690286, 0.06828343, 0.17070858,
                            0.34141715, 0.08535429, 0.11380572],
                           [0.11380572, 0.04877388, 0.34141715, 0.03414172, 0.03793524, 0.05690286, 0.04267714,
                            0.06828343, 0.08535429, 0.17070858]]
                          )


if __name__ == '__main__':
    a = Possible(1, 3, 5, 10)
    print(a.zipf(1))
    a.set_possible_zipf(1)
    print(a.P)
    a.set_certain_zipf()
    print(a.P)
