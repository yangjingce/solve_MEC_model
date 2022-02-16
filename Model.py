import numpy as np
from Delay import Delay
from Possible import Possible
from Task import Task
from Device import Device
from Decision import Decision


class Model:
    def __init__(self):
        # 问题规模
        self.N_cloud = 1  # 云服务器一个
        self.N_FAP = 3  # FAP三个
        self.N_user = 5  # 用户五个
        self.N_device = self.N_cloud + self.N_FAP + self.N_user  # 所有的设备数量
        self.N_task = 10  # 任务的数量
        # 生成延迟矩阵
        delay = Delay(1, 3, 5)
        delay.set_main_delay(
            [(0, 1, 100), (0, 2, 100), (0, 3, 100), (1, 4, 10), (1, 5, 10), (2, 6, 10), (2, 7, 10), (3, 8, 10)])
        delay.convert_direct_to_no()
        delay.find_all_short_path()
        delay.set_between_users_un_arrive()
        self.delay = delay.graph  # 延迟矩阵，D_ij:从i到j的延迟
        # 生成概率矩阵
        possible = Possible(self.N_cloud, self.N_FAP, self.N_user, self.N_task)
        #possible.set_possible_zipf(1)  # 以alpha为参数，生成随机的概率矩阵
        possible.set_certain_zipf()  # 生成确定的zipf分布的概率矩阵
        self.possible = possible.P  # 概率矩阵，P_ur:u用户提出r任务的概率
        # 生成任务
        task = Task(self.N_task)
        task.set_cache()
        task.set_comput()
        self.task_cache = task.Task_cache  # 任务缓存内容的大小
        self.task_comput = task.Task_comput  # 任务计算内容的大小
        # 生成设备
        device = Device(self.N_cloud, self.N_FAP, self.N_user, self.N_task)
        device.set_all()
        self.device_cache = device.cache  # 设备的缓存能力
        self.device_comput = device.comput  # 设备的计算能力
