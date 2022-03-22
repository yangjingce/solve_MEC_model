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
    """本问题是优化排队论模型下的延迟"""

    def __init__(self, model=None):
        if not model:
            model = Model()
        self.model = model
        name = 'MEC_queue_Problem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = self.model.N_user * self.model.N_task  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [Dim - 1] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        x = pop.Phen  # 得到决策变量矩阵
        # 设置用多进程,进程池

        num_cores = int(mp.cpu_count())  # 获得计算机的核心数
        pool = ProcessPool(num_cores)  # 设置池的大小

        # 并行测试代码

        test_data = list(zip([self.model] * pop.sizes, x))
        result = pool.map_async(subAimFunc, test_data)
        result.wait()
        ans_array = np.array(result.get())
        # pop.ObjV = ans_array.copy().reshape(pop.sizes, 1)  # 取出目标函数
        # pop.CV = np.zeros([pop.sizes, 1])  # 取出约束
        pop.ObjV = ans_array[:, 0].copy().reshape(pop.sizes, 1)
        pop.CV = ans_array[:, 1].copy().reshape(pop.sizes, 1)
        pool.close()
        pool.join()

    # def calReferObjV(self):  # 设定目标数参考值（本问题目标函数参考值设定为理论最优值）
    #     return 0


def subAimFunc(args):
    model = args[0]
    order = args[1]
    if_possbile = 0  # 是否此优化顺序满足约束
    # 初始化决策对象
    decision = Decision(model.N_cloud, model.N_FAP, model.N_user, model.N_task, model.device_cache, model.device_comput,
                        model.task_cache, model.task_comput)
    # decision.set_delay(model.delay)
    decision.set_bandwidth(model.bandwidth)
    decision.set_possible(model.possible)
    # 初始解，所有缓存和计算在云端位置上
    decision.cache_position = np.zeros([model.N_device, model.N_task])
    decision.comput_position = np.zeros([model.N_device, model.N_task])
    # 按step步骤优化解
    for step in order:
        step_user = step // model.N_task + model.N_cloud + model.N_FAP
        step_task = step % model.N_task
        if not decision.optimize_device_task_time(step_user, step_task, decision.get_single_device_time):
            if_possbile = 1
    # 计算延迟
    decision.set_device_time()
    return decision.get_max_device_time(), if_possbile
