from Model import Model
from Greedy_algorithm_main import GreedyAlgorithm
from queue_main import QueueAlgorithm
import numpy as np
import pandas as pd
from pylab import *

if __name__ == '__main__':
    N_cloud = 1
    N_FAP = 10
    N_user = 25
    # 实验次数
    N_test = 5
    # 改变用户数
    begin_user = 45
    end_user = 71
    temp_user = list(range(begin_user, end_user, 5))
    # compare_user_ans = np.zeros([N_test, len(temp_user) * 4])
    compare_user_g_ans = np.zeros([N_test + 1, len(temp_user)])
    compare_user_g_time = np.zeros([N_test + 1, len(temp_user)])
    compare_user_q_ans = np.zeros([N_test + 1, len(temp_user)])
    compare_user_q_time = np.zeros([N_test + 1, len(temp_user)])
    same_rate = np.zeros([2, len(temp_user)])
    for i in range(len(temp_user)):
        # g = np.zeros([N_test, 2])
        # q = np.zeros([N_test, 2])
        same_ans_count = 0
        compare_user_g_ans[0, i] = temp_user[i]
        compare_user_g_time[0, i] = temp_user[i]
        compare_user_q_ans[0, i] = temp_user[i]
        compare_user_q_time[0, i] = temp_user[i]
        same_rate[0, i] = temp_user[i]
        for j in range(N_test):

            print('----------', temp_user[i], '----------', j, '------------')
            model = Model(N_cloud, N_FAP, temp_user[i])
            # 博弈算法
            greedy = GreedyAlgorithm(model)
            greedy.solve()
            g_ans, g_cache, g_comput, g_arrive_loop, g_time = greedy.get_result()
            # 遗传算法
            queue = QueueAlgorithm(model)
            queue.solve()
            q_ans, q_cache, q_comput, q_time = queue.get_result()
            # g[j, 0] = g_ans
            # g[j, 1] = g_time
            # q[j, 0] = q_ans
            # q[j, 1] = q_time
            compare_user_g_ans[j + 1, i] = g_ans
            compare_user_g_time[j + 1, i] = g_time
            compare_user_q_ans[j + 1, i] = q_ans
            compare_user_q_time[j + 1, i] = q_time
            if abs(g_ans - q_ans) < 10 ** (-6):
                same_ans_count += 1
        # t = np.hstack([g, q])
        # compare_user_ans[:, i * 4: (i + 1)*4] = t.copy()
        same_rate[1, i] = same_ans_count / N_test
        # 保存文件
        pd.DataFrame(compare_user_g_ans).to_csv(
            str(N_cloud) + '_' + str(N_FAP) + '_' + str(begin_user) + 'to' + str(end_user) + 'g_ans' + '.csv',
            header=False, index=False)
        pd.DataFrame(compare_user_g_time).to_csv(
            str(N_cloud) + '_' + str(N_FAP) + '_' + str(begin_user) + 'to' + str(end_user) + 'g_time' + '.csv',
            header=False, index=False)
        pd.DataFrame(compare_user_q_ans).to_csv(
            str(N_cloud) + '_' + str(N_FAP) + '_' + str(begin_user) + 'to' + str(end_user) + 'q_ans' + '.csv',
            header=False, index=False)
        pd.DataFrame(compare_user_q_time).to_csv(
            str(N_cloud) + '_' + str(N_FAP) + '_' + str(begin_user) + 'to' + str(end_user) + 'q_time' + '.csv',
            header=False, index=False)

        pd.DataFrame(same_rate).to_csv(str(N_cloud) + '_' + str(N_FAP) + '_' + str(begin_user) + 'to' + str(end_user)
                                       + 'same_rate' + '.csv',
                                       header=False, index=False)
    # g = np.zeros([N_test, 2])
    # q = np.zeros([N_test, 2])
    #
    # for i in range(N_test):
    #     print('-----------------', i, '-----------------')
    #     # 生成模型
    #     model = Model()
    #     # 博弈算法
    #     greedy = GreedyAlgorithm(model)
    #     greedy.solve()
    #     g_ans, g_cache, g_comput, g_arrive_loop, g_time = greedy.get_result()
    #     # 遗传算法
    #     queue = QueueAlgorithm(model)
    #     queue.solve()
    #     q_ans, q_cache, q_comput, q_time = queue.get_result()
    #     g[i, 0] = g_ans
    #     q[i, 0] = q_ans
    #
    # t = np.hstack([g, q])
    # x = np.linspace(0, N_test - 1, N_test)
    # plt.plot(x, g)
    # plt.plot(x, q)
    # plt.show()
    #
    # pd.DataFrame(t).to_csv('compare_ans.csv', header=False, index=False)
