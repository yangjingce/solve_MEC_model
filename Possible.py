import numpy as np

class Possible:
    def __init__(self, N_device, N_task):
        self.N_device = N_device
        self.N_task = N_task
        self.P = np.zeros([self.N_device, self.N_task]) # 概率矩阵，P_ur:u用户提出r任务的概率
