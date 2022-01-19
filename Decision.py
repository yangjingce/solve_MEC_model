import numpy as np


class Decision:
    def __init__(self, N_cloud, N_FAP, N_user, N_task):
        self.N_cloud = N_cloud
        self.N_FAP = N_FAP
        self.N_user = N_user
        self.N_device = self.N_cloud + self.N_FAP + self.N_user
        self.N_task = N_task
        self.cache_position = np.zeros([self.N_device, self.N_task])
        self.comput_position = np.zeros([self.N_device, self.N_task])
        self.delay = np.zeros([self.N_device, self.N_device])
        self.possible = np.zeros([self.N_device, self.N_task])
        self.multi_device_exp_delay = np.zeros([1, self.N_device])
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

    def calcul_all_device_exp_delay(self):
        # 计算所有设备的延迟的期望
        for user in range(self.N_device):
            self.multi_device_exp_delay[0, user] = self.calcul_single_device_exp_delay(user)

    def get_max_user_delay(self):
        return max(self.multi_device_exp_delay[0, -self.N_user:])

    def get_average_user_delay(self):
        return sum(self.multi_device_exp_delay[0, -self.N_user:]) / self.N_user


