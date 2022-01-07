# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import numpy as np
import geatpy as ea


# 自定义问题类
class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        # 问题规模
        N_cloud = 1  # 云服务器一个
        N_FAP = 3  # FAP三个
        N_user = 5  # 用户五个
        N_device = N_cloud + N_FAP + N_user  # 所有的设备数量
        N_task = 10  # 任务的数量

        name = 'MEC_Problem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = N_device * N_task * 2  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]  # 决策变量下界
        ub = [N_device]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [0] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        x = pop.Phen  # 得到决策变量矩阵
        pop.ObjV = x * np.sin(10 * np.pi * x) + 2.0  # 计算目标函数值，赋值给pop种群对象的ObjV属性
