import numpy as np
from Decision import Decision
from Model import Model
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool

if __name__ == '__main__':
    model = Model()
    # 设置用多进程,进程池

    num_cores = int(mp.cpu_count())  # 获得计算机的核心数
    pool = ProcessPool(num_cores)  # 设置池的大小

    # 初始解，所有缓存和计算在云端位置上
    ans = np.zeros([2, model.N_device, model.N_task])
    # 初始化决策对象
    decision = Decision(model.N_cloud, model.N_FAP, model.N_user, model.N_task, model.device_cache, model.device_comput, model.task_cache, model.task_comput)
    decision.set_delay(model.delay)
    decision.set_possible(model.possible)
    # 设置初始解
    decision.set_cache_position(ans[0])
    decision.set_comput_position(ans[1])
    # 迭代次数
    N_loop = 1000
    # 算法开始
    priority = np.arange(0, model.N_device, 1) # 优先级矩阵，排在前面的用户先做出卸载决策
    for loop in range(N_loop):

        # 计算当前的解的目标函数
        decision.calcul_every_device_exp_delay()
        cur_objv = decision.get_average_user_delay()  # 目标函数值
        decision.calcul_cache_limit()  # 计算出缓存约束
        decision.calcul_comput_limit()  # 计算出计算约束
        priority = np.argsort(decision.every_device_exp_delay)[0][::-1]
        # 按照优先级矩阵，每个user依次决策
        for user in priority:
            pass

        # 输出当前结果
    # 输出结果



