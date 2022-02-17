import numpy as np
from Decision import Decision
from Model import Model
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool

if __name__ == '__main__':
    # 初始化模型
    model = Model()
    # # 设置用多进程,进程池
    #
    # num_cores = int(mp.cpu_count())  # 获得计算机的核心数
    # pool = ProcessPool(num_cores)  # 设置池的大小

    # 初始解，所有缓存和计算在云端位置上
    ans = np.zeros([2, model.N_device, model.N_task])
    # 初始化决策对象
    decision = Decision(model.N_cloud, model.N_FAP, model.N_user, model.N_task, model.device_cache, model.device_comput,
                        model.task_cache, model.task_comput)
    decision.set_delay(model.delay)
    decision.set_possible(model.possible)
    # 设置初始解
    decision.set_cache_position(ans[0])
    decision.set_comput_position(ans[1])
    # 迭代次数
    N_loop = 5
    # 算法开始
    priority_device = np.arange(0, model.N_device, 1)  # 优先级矩阵，排在前面的device先做出卸载决策
    N_first_device_can_optimize_task = 1  # 优先级最高的device可以优化的task的数量
    min_max_delay = float('inf')  # 最小的最大延迟
    min_ans = None  # 达到最小最大延迟时的卸载决策
    min_arrive_loop = None  # 达到最小最大延迟时的循环次数
    for loop in range(N_loop):

        # 计算当前的解的目标函数
        decision.calcul_every_device_exp_delay()  # 计算每个设备的期望延迟
        decision.calcul_cache_limit()  # 计算出缓存约束
        decision.calcul_comput_limit()  # 计算出计算约束
        priority_device = np.argsort(decision.every_device_exp_delay)[0][::-1]  # 计算优先级，延迟高的优先级高，算法中先优化
        # 按照优先级矩阵，每个device依次决策
        # 对于优先级最高的设备特殊处理

        for task in range(N_first_device_can_optimize_task):
            decision.optimize_device_task(priority_device[0], task)
            decision.calcul_every_device_exp_delay()
            if decision.get_max_user_delay() < min_max_delay:  # 记录最优解
                decision.calcul_every_device_exp_delay()
                min_max_delay = decision.get_max_user_delay()
                min_ans = np.stack((decision.cache_position, decision.comput_position), axis=0)
                min_arrive_loop = loop

        # 按优先级顺序进行处理
        for task in range(model.N_task):
            for i, device in enumerate(priority_device):

                if i == 0 and task < N_first_device_can_optimize_task:
                    pass
                else:
                    decision.optimize_device_task(priority_device[i], task)
                    decision.calcul_every_device_exp_delay()
                    if decision.get_max_user_delay() < min_max_delay:  # 记录最优解
                        min_max_delay = decision.get_max_user_delay()
                        min_ans = np.stack((decision.cache_position, decision.comput_position), axis=0)
                        min_arrive_loop = loop

        decision.calcul_every_device_exp_delay()

        # 输出当前结果
        print(loop, decision.get_max_user_delay())
    # 输出最好结果
    print('-------------------------------------')
    print(min_max_delay)
    print(min_ans)
    print(min_arrive_loop)
