import numpy as np


class Decision:
    def __init__(self, N_cloud, N_FAP, N_user, N_task, cache_ability, comput_ability, task_cache, task_comput):
        self.N_cloud = N_cloud
        self.N_FAP = N_FAP
        self.N_user = N_user
        self.N_device = self.N_cloud + self.N_FAP + self.N_user
        self.N_task = N_task
        self.device_cache = cache_ability  # 设备的缓存能力
        self.device_comput = comput_ability  # 设备的计算能力
        self.task_cache = task_cache
        self.task_comput = task_comput
        self.cache_position = np.zeros([self.N_device, self.N_task])  # 缓存位置
        self.comput_position = np.zeros([self.N_device, self.N_task])  # 计算位置
        self.delay = np.zeros([self.N_device, self.N_device])  # 时延矩阵
        self.possible = np.zeros([self.N_device, self.N_task])  # 概率矩阵
        self.every_device_exp_delay = np.zeros([1, self.N_device])  # 所有设备的延迟期望矩阵
        self.cache_limit = np.zeros([1, self.N_device])  # 缓存约束
        self.comput_limit = np.zeros([1, self.N_device])  # 计算约束
        return

    def set_cache_position(self, cache_position):
        # 设置缓存位置的决策变量
        self.cache_position = cache_position
        return

    def set_comput_position(self, comput_position):
        # 设置计算位置的决策变量
        self.comput_position = comput_position
        return

    def set_delay(self, delay):
        self.delay = delay

    def set_possible(self, possible):
        self.possible = possible

    def calcul_single_device_exp_delay(self, user):
        # 计算单个设备的延迟的期望
        single_device_exp_dalay = 0  # 单个用户的延迟期望
        for task in range(self.N_task):
            single_device_cache_position = int(self.cache_position[user, task])
            single_device_comput_position = int(self.comput_position[user, task])
            single_device_single_task_dalay = self.delay[single_device_cache_position, single_device_comput_position] + \
                                              self.delay[single_device_comput_position, user]
            single_device_exp_dalay += single_device_single_task_dalay * self.possible[user, task]
        return single_device_exp_dalay

    def calcul_every_device_exp_delay(self):
        # 计算所有设备的延迟的期望
        for user in range(self.N_device):
            self.every_device_exp_delay[0, user] = self.calcul_single_device_exp_delay(user)

    def get_max_user_delay(self):
        # 计算所有用户的最大延迟
        return max(self.every_device_exp_delay[0, -self.N_user:])

    def get_average_user_delay(self):
        return sum(self.every_device_exp_delay[0, -self.N_user:]) / self.N_user

    def calcul_cache_limit(self):  # 计算缓存约束
        for device in range(self.N_device):
            sum_cache = 0
            for task in range(self.N_task):
                if device in self.cache_position[:, task]:
                    sum_cache += self.task_cache[task]

            self.cache_limit[0, device] = sum_cache - self.device_cache[0, device]

    def calcul_comput_limit(self):  # 计算计算约束

        for device in range(self.N_device):
            offload_user_task = np.where(self.comput_position == device)
            exp_cal = sum(self.possible[offload_user_task] * self.task_comput[offload_user_task[1]])

            self.comput_limit[0, device] = exp_cal - self.device_comput[0, device]
