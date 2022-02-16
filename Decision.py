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
        self.task_cache = task_cache  # 任务的缓存需求
        self.task_comput = task_comput  # 任务的计算需求
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
        # 返回用户的平均延迟
        return sum(self.every_device_exp_delay[0, -self.N_user:]) / self.N_user

    def calcul_device_cache_limit(self, device):  # 计算单个设备上的缓存约束
        sum_cache = 0
        for task in range(self.N_task):
            if device in self.cache_position[:, task]:
                sum_cache += self.task_cache[task]
        self.cache_limit[0, device] = sum_cache - self.device_cache[0, device]

    def calcul_cache_limit(self):  # 计算所有设备上的缓存约束
        for device in range(self.N_device):
            self.calcul_device_cache_limit(device)

    def calcul_device_comput_limit(self, device):  # 计算单个设备上的计算约束
        offload_user_task = np.where(self.comput_position == device)
        exp_cal = sum(self.possible[offload_user_task] * self.task_comput[offload_user_task[1]])
        self.comput_limit[0, device] = exp_cal - self.device_comput[0, device]

    def calcul_comput_limit(self):  # 计算所有设备上的计算约束
        for device in range(self.N_device):
            self.calcul_device_comput_limit(device)

    def optimize_device_task(self, device, task):  # 改变单个设备单个任务的卸载决策，以优化延迟

        # 寻找可能的缓存位置
        possible_cache_device = []
        cur_cache = int(self.cache_position[device, task])  # 保存原始缓存位置
        for cache_device in range(self.N_device):  # 穷举所有缓存位置
            self.cache_position[device, task] = cache_device  # 设置为新的缓存位置
            # 计算缓存约束
            sum_cache = 0
            for t in range(self.N_task):
                if cache_device in self.cache_position[:, t]:
                    sum_cache += self.task_cache[t]
            cache_limit = sum_cache - self.device_cache[0, cache_device]

            if cache_limit <= 0:  # 如果满足缓存约束
                possible_cache_device.append(cache_device)  # 加入列表
        self.cache_position[device, task] = cur_cache  # 还原为原始缓存位置

        # 寻找可能的计算位置
        possible_comput_device = []
        cur_comput = int(self.comput_position[device, task])  # 保存原始计算位置
        for comput_device in range(self.N_device):  # 穷举所有计算位置
            self.comput_position[device, task] = comput_device  # 设置为新的计算位置
            # 计算计算约束,使用期望计算
            offload_user_task = np.where(self.comput_position == comput_device)
            exp_cal = sum(self.possible[offload_user_task] * self.task_comput[offload_user_task[1]])
            comput_limit = exp_cal - self.device_comput[0, comput_device]

            if comput_limit <= 0:  # 如果满足计算约束
                possible_comput_device.append(comput_device)  # 加入列表
        self.comput_position[device, task] = cur_comput  # 还原为原始缓存位置

        # 寻找更低延迟的位置
        for cache_device in possible_cache_device:
            for comput_device in possible_comput_device:
                if self.delay[cache_device, comput_device] + self.delay[comput_device, device] < \
                        self.delay[int(self.cache_position[device, task]), int(self.comput_position[device, task])] + \
                        self.delay[int(self.comput_position[device, task]), device]:  # 如果时延更小
                    # 设置为新的缓存位置和计算位置
                    self.cache_position[device, task] = cache_device
                    self.comput_position[device, task] = comput_device
