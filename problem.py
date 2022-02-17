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
from Model import Model
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


# 自定义问题类
class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        self.model = Model()
        name = 'MEC_Problem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = self.model.N_device * self.model.N_task * 2  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [self.model.N_device] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [0] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

        # 设置用多进程,进程池

        num_cores = int(mp.cpu_count())  # 获得计算机的核心数
        self.pool = ProcessPool(num_cores)  # 设置池的大小

    def aimFunc(self, pop):  # 目标函数
        x = pop.Phen  # 得到决策变量矩阵
        population_cache = x[:, range(x.shape[1] // 2)]  # 决策变量,缓存位置
        population_cache = np.array(
            [individual.reshape(self.model.N_device, self.model.N_task) for individual in
             population_cache])  # 把每个个体一维的缓存决策变量还原为矩阵
        population_comput = x[:, range(x.shape[1] // 2, x.shape[1])]  # 决策变量，计算位置
        population_comput = np.array(
            [individual.reshape(self.model.N_device, self.model.N_task) for individual in
             population_comput])  # 把每个个体一维的计算决策变量还原为矩阵
        # 设置决策变量类列表

        decison_list = [None] * pop.sizes
        for i in range(pop.sizes):
            s = Decision(self.model.N_cloud, self.model.N_FAP, self.model.N_user, self.model.N_task,
                         self.model.device_cache,
                         self.model.device_comput, self.model.task_cache, self.model.task_comput)
            s.set_delay(self.model.delay)
            s.set_possible(self.model.possible)
            decison_list[i] = s
        # 并行测试代码

        test_data = list(zip(decison_list, population_cache, population_comput))
        result = self.pool.map_async(subAimFunc, test_data)
        result.wait()
        ans_array = np.array(result.get())
        pop.ObjV = ans_array[:, 0].copy().reshape(pop.sizes, 1)  # 取出目标函数
        pop.CV = ans_array[:, 1:].copy()  # 取出约束
        #
        # ObjV = np.zeros([x.shape[0], 1])
        # cv = np.zeros([x.shape[0], self.model.N_device * 2])
        # for i in range(x.shape[0]):
        #     # 计算目标函数
        #     temp.set_cache_position(population_cache[i])
        #     temp.set_comput_position(population_comput[i])
        #     temp.calcul_all_device_exp_delay()
        #     fx_value = temp.get_average_user_delay()
        #     ObjV[i, 0] = fx_value  # 把单个基因的目标函数值保存
        #     # 约束
        #     # 采用可行性法则处理约束
        #     # 缓存容量约束
        #
        #     temp.calcul_cache_limit()
        #     temp.calcul_comput_limit()
        #     cv[i, :] = np.hstack((temp.cache_limit, temp.comput_limit))
        # if x.shape[0] > 1:
        #     print('aaaa')
        #     pass
        # pop.ObjV = ObjV  # 把求得的目标函数值赋值给种群pop的ObjV
        # pop.CV = cv

    def calReferObjV(self):  # 设定目标数参考值（本问题目标函数参考值设定为理论最优值）
        # 测试最优解
        temp = Decision(self.model.N_cloud, self.model.N_FAP, self.model.N_user, self.model.N_task)
        temp.set_delay(self.model.delay)
        temp.set_possible(self.model.possible)
        test_solution = [0] * self.model.N_task + [1] * self.model.N_task + [2] * self.model.N_task + [
            3] * self.model.N_task + [4] * self.model.N_task + [5] * self.model.N_task + [6] * self.model.N_task + [
                            7] * self.model.N_task + [8] * self.model.N_task
        test_solution = np.asarray(test_solution)
        test_solution = test_solution.reshape(self.model.N_device, self.model.N_task)
        temp.set_cache_position(test_solution)
        temp.set_comput_position(test_solution)
        temp.calcul_every_device_exp_delay()
        fx_value = temp.get_average_user_delay()
        return fx_value


def subAimFunc(args):
    decision = args[0]
    decision.set_cache_position(args[1])
    decision.set_comput_position(args[2])
    decision.calcul_every_device_exp_delay()
    # objv = decision.get_average_user_delay()  # 目标函数值为平均用户时延
    objv = decision.get_max_user_delay()  # 目标函数为最大用户时延
    decision.calcul_cache_limit()  # 计算出缓存约束
    decision.calcul_comput_limit()  # 计算出计算约束
    objv_cache_comput = np.hstack((np.array([[objv]]), decision.cache_limit, decision.comput_limit))[
        0]  # 把目标函数值，缓存约束，计算约束放在一个向量里返回
    return objv_cache_comput
