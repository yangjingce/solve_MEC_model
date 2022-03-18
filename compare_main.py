from Model import Model
from Greedy_algorithm_main import GreedyAlgorithm
from order_main import OrderAlgorithm
import numpy as np
import pandas as pd

if __name__ == '__main__':
    N_test = 10
    g = np.zeros([N_test, 1])
    o = np.zeros([N_test, 1])

    for i in range(N_test):
        print('-----------------', i, '-----------------')
        # 生成模型
        model = Model()
        # 博弈算法
        greedy = GreedyAlgorithm(model)
        greedy.solve()
        g_ans, g_cache, g_comput, g_arrive_loop = greedy.get_result()
        # 遗传算法
        order = OrderAlgorithm(model)
        order.solve()
        o_ans, o_cache, o_comput = order.get_result()
        g[i, 0] = g_ans
        o[i, 0] = o_ans

    t = np.hstack([g, o])
    pd.DataFrame(t).to_csv('compare_ans.csv')



