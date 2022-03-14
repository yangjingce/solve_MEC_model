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
        self.bandwidth = np.zeros([self.N_device, self.N_device])  # 带宽矩阵
        self.possible = np.zeros([self.N_device, self.N_task])  # 概率矩阵
        self.every_device_exp_delay = np.zeros([1, self.N_device])  # 所有设备的延迟期望矩阵
        self.every_device_every_task_exp_delay = np.zeros([self.N_device, self.N_task])  # 每个设备每个任务延迟期望

        self.every_device_time = np.zeros([1, self.N_device])  # 所有设备的延迟期望矩阵,带宽情况下
        self.every_device_every_task_time = np.zeros([self.N_device, self.N_task])  # 每个设备每个任务延迟期望，带宽情况下
        self.cache_limit = np.zeros([1, self.N_device])  # 缓存约束
        self.comput_limit = np.zeros([1, self.N_device])  # 计算约束
        return

    def set_cache_position(self, cache_position):
        """设置缓存位置的决策变量"""
        self.cache_position = cache_position
        return

    def set_comput_position(self, comput_position):
        """设置计算位置的决策变量"""
        self.comput_position = comput_position
        return

    def set_delay(self, delay):
        """设置延迟矩阵"""
        self.delay = delay

    def set_bandwidth(self, bandwidth):
        """设置带宽矩阵"""
        self.bandwidth = bandwidth

    def set_possible(self, possible):
        """设置设备提出概率的矩阵"""
        self.possible = possible

    def calcul_single_device_single_task_exp_delay(self, device, task):
        """计算单个设备单个任务的延迟的期望,已经乘了概率"""
        cache_position = int(self.cache_position[device, task])
        comput_position = int(self.comput_position[device, task])
        delay = self.delay[cache_position, comput_position] + self.delay[comput_position, device]
        self.every_device_every_task_exp_delay[device, task] = delay * self.possible[device, task]
        return

    def calcul_single_device_exp_delay(self, device):
        """计算单个设备的延迟的期望"""
        for task in range(self.N_task):
            self.calcul_single_device_single_task_exp_delay(device, task)
        self.every_device_exp_delay[0, device] = sum(self.every_device_every_task_exp_delay[device, :])
        return

    def calcul_every_device_exp_delay(self):
        """计算所有设备的延迟的期望"""
        for device in range(self.N_device):
            self.calcul_single_device_exp_delay(device)

    def get_max_user_delay(self):
        """计算所有用户的最大延迟"""
        return max(self.every_device_exp_delay[0, -self.N_user:])

    def get_average_user_delay(self):
        """返回用户的平均延迟"""
        return sum(self.every_device_exp_delay[0, -self.N_user:]) / self.N_user

    def calcul_device_cache_limit(self, device):
        """计算单个设备上的缓存约束,结果放入矩阵"""
        sum_cache = 0
        for task in range(self.N_task):
            if device in self.cache_position[:, task]:
                sum_cache += self.task_cache[task]
        self.cache_limit[0, device] = sum_cache - self.device_cache[0, device]

    def calcul_cache_limit(self):
        """计算所有设备上的缓存约束,结果放入矩阵"""
        for device in range(self.N_device):
            self.calcul_device_cache_limit(device)

    def calcul_device_comput_limit(self, device):
        """计算单个设备上的计算约束，结果放入矩阵"""
        offload_user_task = np.where(self.comput_position == device)
        sum_cal = sum(self.task_comput[offload_user_task[1]])  # 考虑最大的计算负载小于设备的计算能力
        self.comput_limit[0, device] = sum_cal - self.device_comput[0, device]

    def calcul_comput_limit(self):
        """计算所有设备上的计算约束，结果放入矩阵"""
        for device in range(self.N_device):
            self.calcul_device_comput_limit(device)

    def optimize_device_task_delay(self, device, task):
        """改变单个设备单个任务的卸载决策，以优化延迟"""
        possible_cache_device = self.find_possible_cache_device(device, task)
        possible_comput_device = self.find_possible_comput_device(device, task)

        # 寻找更低延迟的位置
        for cache_device in possible_cache_device:
            for comput_device in possible_comput_device:
                if self.delay[cache_device, comput_device] + self.delay[comput_device, device] < \
                        self.delay[int(self.cache_position[device, task]), int(self.comput_position[device, task])] + \
                        self.delay[int(self.comput_position[device, task]), device]:  # 如果时延更小
                    # 设置为新的缓存位置和计算位置
                    self.cache_position[device, task] = cache_device
                    self.comput_position[device, task] = comput_device

    def calcul_single_device_offload_single_device_single_task_arrive_rate(self, source_device, target_device, task):
        """求单个device到单个device的单个task的到达率"""
        if self.comput_position[source_device, task] == target_device:
            return self.possible[source_device, task] * self.task_comput[task]
        else:
            return 0

    def calcul_single_device_offload_single_device_arrive_rate(self, source_device, target_device):
        """求单个device到单个device的到达率"""
        arrive_rate = 0
        for request_task in range(self.N_task):
            arrive_rate += self.calcul_single_device_offload_single_device_single_task_arrive_rate(source_device,
                                                                                                   target_device,
                                                                                                   request_task)
        return arrive_rate

    def calcul_single_device_arrive_rate(self, target_device):
        """求单个device的到达率"""
        arrive_rate = 0
        for source_device in range(self.N_device):
            arrive_rate += self.calcul_single_device_offload_single_device_arrive_rate(source_device, target_device)
        return arrive_rate

    def calcul_single_device_service_strength(self, device):
        """求device处的服务强度"""
        return self.calcul_single_device_arrive_rate(device) / self.device_comput[0, device]

    def calcul_single_device_wait_time(self, device):
        """求任务在device处排队的平均等待时间"""
        rho = self.calcul_single_device_service_strength(device)
        f = self.device_comput[0, device]
        return rho / (f * (1 - rho))

    def calcul_single_device_single_task_process_time(self, device, task):
        """任务在device处处理的时间"""
        return self.task_comput[task] / self.device_comput[0, device]

    def calcul_single_device_single_task_all_time(self, device, task):
        """任务在device处计算总共的时间"""
        if self.task_comput[task] == 0:  # 如果不需要计算,不用等待，直接返回0
            return 0
        else:  # 否则，包含等待和处理两部分时间
            return self.calcul_single_device_wait_time(device) + \
               self.calcul_single_device_single_task_process_time(device, task)

    def calcul_task_transmit_time(self, source_device, target_device, task):
        """任务在节点间传输的时间"""
        if source_device == target_device:
            return 0
        else:
            return self.task_cache[task] / self.bandwidth[source_device, target_device]

    def calcul_transmit_comput_transmit_time(self, cache_device, comput_device, end_device, task):
        """传输计算再传输的时间"""
        return self.calcul_task_transmit_time(cache_device, comput_device, task) + \
               self.calcul_single_device_single_task_all_time(comput_device, task) + \
               self.calcul_task_transmit_time(comput_device, end_device, task)

    def calcul_single_device_single_task_time(self, end_device, task):
        """用户在提出单个任务的期望延迟"""
        return self.calcul_transmit_comput_transmit_time(int(self.cache_position[end_device, task]),
                                                         int(self.comput_position[end_device, task]),
                                                         end_device, task)

    def calcul_single_device_time(self, device):
        """设备提出任务的期望延迟"""
        exp_time = 0
        for task in range(self.N_task):
            exp_time += self.possible[device, task] * self.calcul_single_device_single_task_time(device, task)
        return exp_time

    def find_possible_cache_device(self, device, task):
        """寻找可能的缓存位置"""
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
        return possible_cache_device

    def find_possible_comput_device(self, device, task):
        """寻找可能的计算位置"""
        possible_comput_device = []
        cur_comput = int(self.comput_position[device, task])  # 保存原始计算位置
        for comput_device in range(self.N_device):  # 穷举所有计算位置
            self.comput_position[device, task] = comput_device  # 设置为新的计算位置
            # 计算计算约束,使用最大值计算
            offload_user_task = np.where(self.comput_position == comput_device)
            exp_cal = sum(self.task_comput[offload_user_task[1]])
            comput_limit = exp_cal - self.device_comput[0, comput_device]

            if comput_limit <= 0:  # 如果满足计算约束
                possible_comput_device.append(comput_device)  # 加入列表
        self.comput_position[device, task] = cur_comput  # 还原为原始缓存位置
        return possible_comput_device

    def optimize_device_task_time(self, device, task, function):
        """改变单个设备单个任务的卸载决策，以优化排队论下的延迟"""
        possible_cache_device = self.find_possible_cache_device(device, task)
        possible_comput_device = self.find_possible_comput_device(device, task)
        # 记录最好位置
        best_cache_position = self.cache_position[device, task]
        best_comput_position = self.comput_position[device, task]
        best_value = function(device, task)
        # 寻找更低延迟的位置
        for cache_device in possible_cache_device:
            self.cache_position[device, task] = cache_device
            for comput_device in possible_comput_device:
                self.comput_position[device, task] = comput_device
                if function(device, task) < best_value:
                    # 记录最好位置
                    best_cache_position = self.cache_position[device, task]
                    best_comput_position = self.comput_position[device, task]
                    best_value = function(device, task)
        # 使用最好位置
        self.cache_position[device, task] = best_cache_position
        self.comput_position[device, task] = best_comput_position




    def set_single_device_single_task_time(self, device, task):
        """计算单个设备单个任务的时延，放入矩阵，在排队论下"""
        self.every_device_every_task_time[device, task] \
            = self.calcul_single_device_single_task_time(device, task) * self.possible[device, task]

    def set_every_device_every_task_time(self):
        """计算所有设备所有任务的时延，放入矩阵，在排队论下"""
        for device in range(self.N_device):
            for task in range(self.N_task):
                self.set_single_device_single_task_time(device, task)

    def set_single_device_time(self, device):
        """计算单个设备的期望时延，排队论下"""
        for task in range(self.N_task):
            self.set_single_device_single_task_time(device, task)

        self.every_device_time[0, device] = sum(self.every_device_every_task_time[device, :])

    def get_single_device_time(self, device, task):
        """计算单个设备的延迟期望并返回，专为optimize函数设计，作为函数指针传入"""
        self.set_single_device_time(device)
        return self.every_device_time[0, device]

    def set_device_time(self):
        """计算所有设备的期望时延，排队论下"""
        for device in range(self.N_device):
            self.set_single_device_time(device)

    def get_max_device_time(self):
        """返回所有用户最大的期望延迟，排队论下"""
        return self.every_device_time.max()




