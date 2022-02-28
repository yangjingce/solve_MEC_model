import numpy as np
from Decision import Decision
from Model import Model
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool
import time
import itertools
if __name__=='__main__':
    # 穷举方法，一个用户优化一个任务作为一个步骤，穷举所有步骤
    # 时间复杂度太高，无法穷举做

    # 初始化模型
    model = Model()


    # 初始化决策对象
    decision = Decision(model.N_cloud, model.N_FAP, model.N_user, model.N_task, model.device_cache, model.device_comput,
                        model.task_cache, model.task_comput)
    decision.set_delay(model.delay)
    decision.set_possible(model.possible)

    min_max_delay = float('inf')
    min_ans = None
    # 穷举开始
    T1 = time.perf_counter()
    count = 10**4
    for order in itertools.permutations(range(model.N_user*model.N_task)):
        # 初始解，所有缓存和计算在云端位置上
        decision.cache_position = np.zeros([model.N_device, model.N_task])
        decision.comput_position = np.zeros([model.N_device, model.N_task])
        # 按step步骤优化解
        for step in order:
            step_user = step // model.N_task + model.N_cloud + model.N_FAP
            step_task = step % model.N_task
            decision.optimize_device_task(step_user, step_task)
        # 计算延迟
        decision.calcul_every_device_exp_delay()
        if decision.get_max_user_delay() < min_max_delay:  # 记录最优解
            min_max_delay = decision.get_max_user_delay()
            min_ans = order
        count -= 1
        if count < 0:
            break

    T2 = time.perf_counter()
    print('程序运行时间：%s毫秒'%(T2 - T1))
