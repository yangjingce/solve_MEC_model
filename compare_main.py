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
        model = Model()
        g_ans, g_cache, g_comput, g_arrive_loop = GreedyAlgorithm(model)
        o_ans, o_cache, o_comput = OrderAlgorithm(model)
        g[0, i] = g_ans
        o[0, i] = o_ans
    t = np.hstack([g, o])
    pd.DataFrame(t).to_csv('compare_ans.csv')



