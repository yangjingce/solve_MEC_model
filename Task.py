import numpy as np

class Task:
    def __init__(self, N_task):
        self.N_task = N_task
        self.Task_cache = np.zeros([1, self.N_task])   # 任务缓存内容的大小
        self.Task_comput = np.zeros([1, self.N_task])  # 任务计算内容的大小
    def set_cache(self):
        self.Task_cache = np.array([])




    def set_comput(self):
        self.Task_comput = np.array([])

