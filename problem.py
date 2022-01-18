# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import numpy as np
import geatpy as ea
import Delay

# 自定义问题类
class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        # 问题规模
        self.N_cloud = 1  # 云服务器一个
        self.N_FAP = 3  # FAP三个
        self.N_user = 5  # 用户五个
        self.N_device = self.N_cloud + self.N_FAP + self.N_user  # 所有的设备数量
        self.N_task = 10  # 任务的数量
        self.D = np.empty([self.N_device, self.N_device])  # 延迟矩阵，D_ij:从i到j的延迟
        #
        self.P = np.empty([self.N_device, self.N_task])  # 概率矩阵，P_ur:u用户提出r任务的概率
        self.TA = np.empty([1, self.N_task])  # 任务缓存内容的大小
        self.TB = np.empty([1, self.N_task])  # 任务计算内容的大小
        self.A = np.empty([1, self.N_device])  # 缓存能力
        self.B = np.empty([1, self.N_device])  # 计算能力

        name = 'MEC_Problem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = self.N_device * self.N_task * 2  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]  # 决策变量下界
        ub = [self.N_device]  # 决策变量上界
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

        # 计算目标函数
        ObjV = []
        for i in range(x.shape[0]):
            multi_user_exp_delay = []  # 所有用户的延迟期望
            for user in range(self.N_device):
                single_user_exp_dalay = 0  # 单个用户的延迟期望
                for task in range(self.N_task):
                    single_user_single_task_delay = self.D[CA[i][user][task], CB[i][user][task]] + self.D[
                        CB[i][user][task], user]
                    single_user_exp_dalay += single_user_single_task_delay * self.P[user, task]
                multi_user_exp_delay.append(single_user_exp_dalay)
            ObjV.append(max(multi_user_exp_delay))  # 把单个基因的目标函数值保存，目标函数为最大的单用户期望延迟
        pop.ObjV = np.array([ObjV]).T  # 把求得的目标函数值赋值给种群pop的ObjV

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
                        sum_cache += self.TA[task]
                A_bound.append(sum_cache - self.A[device])

            B_bound = []
            for device in range(self.N_device):
                exp_cal = 0
                for user in range(self.N_device):
                    for task in range(self.N_task):
                        if CB[i][user][task] == device:
                            exp_cal += self.P[user][task] * self.TB[task]
                B_bound.append(exp_cal - self.B[device])
            cv.append(A_bound + B_bound)

        pop.CV = np.array(cv)

    # def calReferObjV(self):  # 设定目标数参考值（本问题目标函数参考值设定为理论最优值）
    #     referenceObjV = np.array([[2.5]])
    #     return referenceObjV
