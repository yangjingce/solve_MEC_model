import numpy as np
from Decision import Decision
from Model import Model
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool
import time
from Device import Device


class GreedyAlgorithm:
    def __init__(self, model):
        self.model = model
        self.decision = None
        self.min_max_delay = float('inf')  # 最小的最大延迟
        self.min_ans = None  # 达到最小最大延迟时的卸载决策
        self.min_arrive_loop = None  # 达到最小最大延迟时的循环次数
        self.spend_time = None  # 运行算法花费的时间

    def solve(self):
        begin_time = time.process_time()
        # 初始化决策对象
        decision = Decision(self.model.N_cloud, self.model.N_FAP, self.model.N_user, self.model.N_task,
                            self.model.device_cache,
                            self.model.device_comput, self.model.task_cache, self.model.task_comput)
        decision.set_bandwidth(self.model.bandwidth)
        decision.set_possible(self.model.possible)
        # 设置初始解，所有缓存和计算在云端位置上
        decision.set_cache_position(np.zeros([self.model.N_device, self.model.N_task]))
        decision.set_comput_position(np.zeros([self.model.N_device, self.model.N_task]))
        # 迭代次数
        N_loop = 3
        # 算法开始
        priority_device = np.arange(0, self.model.N_device, 1)  # 优先级矩阵，排在前面的device先做出卸载决策
        N_first_device_can_optimize_task = 1  # 优先级最高的device可以优化的task的数量
        first_device = None  # 上次优先级最高的device

        for loop in range(N_loop):

            # 计算当前的解的目标函数
            # decision.calcul_every_device_exp_delay()  # 计算每个设备的期望延迟
            decision.set_device_time()
            decision.calcul_cache_limit()  # 计算出缓存约束
            decision.calcul_comput_limit()  # 计算出计算约束
            # priority_device = np.argsort(decision.every_device_exp_delay)[0][::-1]  # 计算优先级，延迟高的优先级高，算法中先优化
            priority_device = np.argsort(decision.every_device_time)[0][::-1]
            # 计算每个设备选择任务的优先级
            # priority_device_task = np.array([np.argsort(d)[::-1] for d in decision.every_device_every_task_exp_delay])
            priority_device_task = np.array([np.argsort(d)[::-1] for d in decision.every_device_every_task_time])
            # 按照优先级矩阵，每个device依次决策
            # 判断当前是否优先级最高的设备为上次优先级最高的设备
            if priority_device[0] == first_device:  # 是，增加他可以优化的task的数量
                N_first_device_can_optimize_task = min(N_first_device_can_optimize_task + 1, self.model.N_device)
            else:  # 否，task数量置1
                first_device = priority_device[0]
                N_first_device_can_optimize_task = 1

            # 在进行本轮博弈前，把解重新设为初始解
            decision.set_cache_position(np.zeros([self.model.N_device, self.model.N_task]))
            decision.set_comput_position(np.zeros([self.model.N_device, self.model.N_task]))

            # 对于优先级最高的设备特殊处理
            if_possible = True
            for task in range(N_first_device_can_optimize_task):
                # decision.optimize_device_task_delay(priority_device[0], priority_device_task[priority_device[0], task])
                if not decision.optimize_device_task_time(priority_device[0],
                                                          priority_device_task[priority_device[0], task],
                                                          decision.get_single_device_time):
                    if_possible = False

                # decision.calcul_every_device_exp_delay()
                # if decision.get_max_user_delay() < min_max_delay:  # 记录最优解
                #     decision.calcul_every_device_exp_delay()
                #     min_max_delay = decision.get_max_user_delay()
                #     min_ans = np.stack((decision.cache_position, decision.comput_position), axis=0)
                #     min_arrive_loop = loop

                decision.set_device_time()
                if decision.get_max_device_time() < self.min_max_delay and if_possible:
                    self.min_max_delay = decision.get_max_device_time()
                    self.min_ans = np.stack((decision.cache_position, decision.comput_position), axis=0)
                    self.min_arrive_loop = loop

            # 按优先级顺序进行处理
            for task in range(self.model.N_task):
                for i, device in enumerate(priority_device):

                    if i == 0 and task < N_first_device_can_optimize_task:
                        pass
                    else:
                        # decision.optimize_device_task_delay(priority_device[i], priority_device_task[priority_device[i], task])
                        if not decision.optimize_device_task_time(priority_device[i],
                                                                  priority_device_task[priority_device[i], task],
                                                                  decision.get_single_device_time):
                            if_possible = False

                        # decision.calcul_every_device_exp_delay()
                        # if decision.get_max_user_delay() < min_max_delay:  # 记录最优解
                        #     min_max_delay = decision.get_max_user_delay()
                        #     min_ans = np.stack((decision.cache_position, decision.comput_position), axis=0)
                        #     min_arrive_loop = loop

                        decision.set_device_time()
                        if decision.get_max_device_time() < self.min_max_delay and if_possible:
                            self.min_max_delay = decision.get_max_device_time()
                            self.min_ans = np.stack((decision.cache_position, decision.comput_position), axis=0)
                            self.min_arrive_loop = loop

            # decision.calcul_every_device_exp_delay()
            decision.set_device_time()
            # 输出当前结果
            # print(loop, decision.get_max_user_delay())
            if if_possible:
                print(loop, decision.get_max_device_time())
            else:
                print(loop, 'not possible')
        self.decision = decision
        end_time = time.process_time()
        self.spend_time = (end_time - begin_time)

    def print(self):
        """输出最好结果"""
        print(self.min_max_delay)
        print(self.min_ans)
        print(self.min_arrive_loop)

    def get_result(self):
        return self.min_max_delay, self.min_ans[0], self.min_ans[1], self.min_arrive_loop, self.spend_time


if __name__ == '__main__':
    model = Model(1,10,25)
    device = Device(1,10,25,10,1000,30,5,2000,130,5)
    device.set_all()
    model.device_cache = device.device_cache  # 设备的缓存能力
    model.device_comput = device.device_comput  # 设备的计算能力

    t = GreedyAlgorithm(model)
    t.solve()
    g_ans, g_cache, g_comput, g_arrive_loop, g_time = t.get_result()
    print(g_cache)
    print(g_comput)

    # t.print()
