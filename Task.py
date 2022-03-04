import numpy as np

class Task:
    def __init__(self, N_task):
        self.N_task = N_task
        self.task_cache = np.zeros([1, self.N_task])   # 任务缓存内容的大小
        self.task_comput = np.zeros([1, self.N_task])  # 任务计算内容的大小
    def set_cache(self):
        self.task_cache = np.array([0, 0, 0, 10, 10, 20, 20, 50, 50, 100])




    def set_comput(self):
        self.task_comput = np.array([100, 50, 50, 20, 20, 10, 10, 0, 0, 0])

if __name__ == "__main__":
    a = Task(10)
    a.set_cache()
    a.set_comput()
    print(a.task_cache)
    print(a.task_comput)
