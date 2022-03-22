import numpy as np
from Delay import Delay
from Possible import Possible
from Task import Task
from Device import Device
from Decision import Decision
from BandWidth import Bandwidth


class Model:
    def __init__(self, N_cloud=1, N_FAP=3, N_user=5, N_task=10):
        # 问题规模
        self.N_cloud = N_cloud
        """云服务器数量"""
        self.N_FAP = N_FAP
        """FAP数量"""
        self.N_user = N_user
        """用户数量"""
        self.N_device = self.N_cloud + self.N_FAP + self.N_user
        """所有设备的数量"""
        self.N_task = N_task
        """任务的数量"""
        # # 生成延迟矩阵
        # delay = Delay(self.N_cloud, self.N_FAP, self.N_user)
        # # 设置关键节点之间的延迟
        # delay.set_main_delay(
        #     [(0, 1, 100), (0, 2, 100), (0, 3, 100), (1, 4, 10), (1, 5, 10), (2, 6, 10), (2, 7, 10), (3, 8, 10)])
        # delay.convert_direct_to_no()
        # delay.find_all_short_path()
        # delay.set_between_users_un_arrive()
        # self.delay = delay.graph  # 延迟矩阵，D_ij:从i到j的延迟
        # 生成带宽矩阵类
        bandwidth = Bandwidth(self.N_cloud, self.N_FAP, self.N_user)
        # 设置关键节点之间的带宽
        # bandwidth.set_main_bandwidth([(0, 1, 10), (0, 2, 10), (0, 3, 10), (1, 4, 100),
        #                               (1, 5, 100), (2, 6, 100), (2, 7, 100), (3, 8, 100)])
        bandwidth.set_main_bandwidth(bandwidth.generate_main_bandwidth(100, 10))
        bandwidth.convert_direct_to_no()
        bandwidth.find_all_bandwidth_path()
        bandwidth.set_device_self_bandwidth_None()
        self.bandwidth = bandwidth.graph  # 带宽矩阵，B_ij:从i到j的带宽，B_ii的带宽为None
        # 生成概率矩阵
        possible = Possible(self.N_cloud, self.N_FAP, self.N_user, self.N_task)
        possible.set_possible_zipf(1)  # 以alpha为参数，生成随机的概率矩阵
        # possible.set_certain_zipf()  # 生成确定的zipf分布的概率矩阵
        self.possible = possible.P  # 概率矩阵，P_ur:u用户提出r任务的概率
        # 生成任务
        task = Task(self.N_task)
        task.set_cache()
        task.set_comput()
        self.task_cache = task.task_cache  # 任务缓存内容的大小
        self.task_comput = task.task_comput  # 任务计算内容的大小
        # 生成设备
        device = Device(self.N_cloud, self.N_FAP, self.N_user, self.N_task)
        device.set_all()
        self.device_cache = device.device_cache  # 设备的缓存能力
        self.device_comput = device.device_comput  # 设备的计算能力
