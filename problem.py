# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import numpy as np
import geatpy as ea
from Delay import Delay
from Possible import Possible
from Task import Task
from Device import Device
from Decision import Decision


# 自定义问题类
class MyProblem(ea.Problem):  # 继承Problem父类
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
        self.D = delay.graph  # 延迟矩阵，D_ij:从i到j的延迟
        # 生成概率矩阵
        possible = Possible(self.N_cloud, self.N_FAP, self.N_user, self.N_task)
        possible.set_possible_zipf(1)
        self.P = possible.P  # 概率矩阵，P_ur:u用户提出r任务的概率
        # 生成任务
        task = Task(self.N_task)
        task.set_cache()
        task.set_comput()
        self.Task_cache = task.Task_cache  # 任务缓存内容的大小
        self.Task_comput = task.Task_comput  # 任务计算内容的大小
        # 生成设备
        device = Device(self.N_cloud, self.N_FAP, self.N_user, self.N_task)
        device.set_all()
        self.A = device.cache  # 缓存能力
        self.B = device.comput  # 计算能力

        name = 'MEC_Problem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = self.N_device * self.N_task * 2  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [self.N_device] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [0] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        x = pop.Phen  # 得到决策变量矩阵
        CA = x[:, range(x.shape[1] // 2)]  # 决策变量,缓存位置
        CA = np.array([individual.reshape(self.N_device, self.N_task) for individual in CA])  # 把每个个体一维的缓存决策变量还原为矩阵
        CB = x[:, range(x.shape[1] // 2, x.shape[1])]  # 决策变量，计算位置
        CB = np.array([individual.reshape(self.N_device, self.N_task) for individual in CB])  # 把每个个体一维的计算决策变量还原为矩阵
        # 设置决策变量类
        temp = Decision(self.N_cloud, self.N_FAP, self.N_user, self.N_task)
        temp.set_delay(self.D)
        temp.set_possible(self.P)
        # 计算目标函数
        ObjV = np.zeros([x.shape[0],1])
        for i in range(x.shape[0]):
            temp.set_cache_position(CA[i])
            temp.set_comput_position(CB[i])

            temp.calcul_all_device_exp_delay()
            fx_value = temp.get_average_user_delay()
            ObjV[i, 0] = fx_value  # 把单个基因的目标函数值保存
        pop.ObjV = ObjV  # 把求得的目标函数值赋值给种群pop的ObjV

        # 约束
        # 采用可行性法则处理约束
        cv = []
        for i in range(x.shape[0]):
            # 缓存容量约束
            A_bound = []
            for device in range(self.N_device):
                sum_cache = 0
                for task in range(self.N_task):
                    if_cache = False
                    for user in range(self.N_device):
                        if CA[i, user, task] == device:
                            if_cache = True
                            break
                    if if_cache:
                        sum_cache += self.Task_cache[task]
                A_bound.append(sum_cache - self.A[0, device])

            B_bound = []
            for device in range(self.N_device):
                exp_cal = 0
                for user in range(self.N_device):
                    for task in range(self.N_task):
                        if CB[i][user][task] == device:
                            exp_cal += self.P[user][task] * self.Task_comput[task]
                B_bound.append(exp_cal - self.B[0, device])
            cv.append(A_bound + B_bound)

        pop.CV = np.array(cv)

    # def calReferObjV(self):  # 设定目标数参考值（本问题目标函数参考值设定为理论最优值）
    #     referenceObjV = np.array([[2.5]])
    #     return referenceObjV
