from Model import Model
from Greedy_algorithm_main import GreedyAlgorithm
from queue_main import QueueAlgorithm
import numpy as np
import pandas as pd
from pylab import *
if __name__ == '__main__':
    N_test = 10
    g = np.zeros([N_test, 1])
    q = np.zeros([N_test, 1])

    for i in range(N_test):
        print('-----------------', i, '-----------------')
        # 生成模型
        model = Model()
        # 博弈算法
        greedy = GreedyAlgorithm(model)
        greedy.solve()
        g_ans, g_cache, g_comput, g_arrive_loop, g_time = greedy.get_result()
        # 遗传算法
        queue = QueueAlgorithm(model)
        queue.solve()
        q_ans, q_cache, q_comput, q_time = queue.get_result()
        g[i, 0] = g_ans
        q[i, 0] = q_ans

    t = np.hstack([g, q])
    x = np.linspace(0,N_test -1,N_test)
    plt.plot(x, g)
    plt.plot(x, q)
    plt.show()

    pd.DataFrame(t).to_csv('compare_ans.csv', header=False, index=False)



