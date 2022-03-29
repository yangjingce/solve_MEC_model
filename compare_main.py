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
    # 改变的变量
    change_var = 'fap'
    if change_var == 'user':
        # 改变用户数
        begin_user = 45
        end_user = 71
        temp_user = list(range(begin_user, end_user, 5))

        compare_user_g_ans = np.zeros([N_test + 1, len(temp_user)])
        compare_user_g_time = np.zeros([N_test + 1, len(temp_user)])
        compare_user_q_ans = np.zeros([N_test + 1, len(temp_user)])
        compare_user_q_time = np.zeros([N_test + 1, len(temp_user)])
        same_rate = np.zeros([2, len(temp_user)])
        for i in range(len(temp_user)):
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
                compare_user_g_ans[j + 1, i] = g_ans
                compare_user_g_time[j + 1, i] = g_time
                compare_user_q_ans[j + 1, i] = q_ans
                compare_user_q_time[j + 1, i] = q_time
                if abs(g_ans - q_ans) < 10 ** (-6):
                    same_ans_count += 1

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
            pd.DataFrame(same_rate).to_csv(
                str(N_cloud) + '_' + str(N_FAP) + '_' + str(begin_user) + 'to' + str(end_user)
                + 'same_rate' + '.csv',
                header=False, index=False)
    elif change_var == 'fap':
        # 改变的fap数
        begin_fap = 3
        end_fap = 25
        temp_fap = list(range(begin_fap, end_fap, 3))

        compare_fap_g_ans = np.zeros([N_test + 1, len(temp_fap)])
        compare_fap_g_time = np.zeros([N_test + 1, len(temp_fap)])
        compare_fap_q_ans = np.zeros([N_test + 1, len(temp_fap)])
        compare_fap_q_time = np.zeros([N_test + 1, len(temp_fap)])
        same_rate = np.zeros([2, len(temp_fap)])
        for i in range(len(temp_fap)):
            same_ans_count = 0
            compare_fap_g_ans[0, i] = temp_fap[i]
            compare_fap_g_time[0, i] = temp_fap[i]
            compare_fap_q_ans[0, i] = temp_fap[i]
            compare_fap_q_time[0, i] = temp_fap[i]
            same_rate[0, i] = temp_fap[i]
            for j in range(N_test):
                print('----------', temp_fap[i], '----------', j, '------------')
                model = Model(N_cloud, temp_fap[i], N_user)
                # 博弈算法
                greedy = GreedyAlgorithm(model)
                greedy.solve()
                g_ans, g_cache, g_comput, g_arrive_loop, g_time = greedy.get_result()
                # 遗传算法
                queue = QueueAlgorithm(model)
                queue.solve()
                q_ans, q_cache, q_comput, q_time = queue.get_result()
                compare_fap_g_ans[j + 1, i] = g_ans
                compare_fap_g_time[j + 1, i] = g_time
                compare_fap_q_ans[j + 1, i] = q_ans
                compare_fap_q_time[j + 1, i] = q_time
                if abs(g_ans - q_ans) < 10 ** (-6):
                    same_ans_count += 1

            same_rate[1, i] = same_ans_count / N_test
            # 保存文件
            pd.DataFrame(compare_fap_g_ans).to_csv(
                str(N_cloud) + '_' + str(begin_fap) + 'to' + str(end_fap) + '_' + str(N_user) + 'g_ans' + '.csv',
                header=False, index=False)
            pd.DataFrame(compare_fap_g_time).to_csv(
                str(N_cloud) + '_' + str(begin_fap) + 'to' + str(end_fap) + '_' + str(N_user) + 'g_time' + '.csv',
                header=False, index=False)
            pd.DataFrame(compare_fap_q_ans).to_csv(
                str(N_cloud) + '_' + str(begin_fap) + 'to' + str(end_fap) + '_' + str(N_user) + 'q_ans' + '.csv',
                header=False, index=False)
            pd.DataFrame(compare_fap_q_time).to_csv(
                str(N_cloud) + '_' + str(begin_fap) + 'to' + str(end_fap) + '_' + str(N_user) + 'q_time' + '.csv',
                header=False, index=False)
            pd.DataFrame(same_rate).to_csv(str(N_cloud) + '_' + str(begin_fap) + 'to' + str(end_fap) + '_' + str(N_user)
                                           + 'same_rate' + '.csv',
                                           header=False, index=False)
    else:
        # 改变能力
        begin = 0.5
        end = 2
        temp = np.linespace(begin, end, 10)

        compare_g_ans = np.zeros([N_test + 1, len(temp)])
        compare_g_time = np.zeros([N_test + 1, len(temp)])
        compare_q_ans = np.zeros([N_test + 1, len(temp)])
        compare_q_time = np.zeros([N_test + 1, len(temp)])
        same_rate = np.zeros([2, len(temp)])
        for i in range(len(temp)):
            same_ans_count = 0
            compare_g_ans[0, i] = temp[i]
            compare_g_time[0, i] = temp[i]
            compare_q_ans[0, i] = temp[i]
            compare_q_time[0, i] = temp[i]
            same_rate[0, i] = temp[i]
            for j in range(N_test):
                print('----------', temp[i], '----------', j, '------------')
                if change_var == 'cloud_cache':
                    model = Model(N_cloud, N_FAP, N_user, cache_times=(temp[i], 1, 1), comput_times=(1, 1, 1))
                elif change_var == 'fap_cache':
                    model = Model(N_cloud, N_FAP, N_user, cache_times=(1, temp[i], 1), comput_times=(1, 1, 1))
                elif change_var == 'user_cache':
                    model = Model(N_cloud, N_FAP, N_user, cache_times=(1, 1, temp[i]), comput_times=(1, 1, 1))
                elif change_var == 'cloud_comput':
                    model = Model(N_cloud, N_FAP, N_user, cache_times=(1, 1, 1), comput_times=(temp[i], 1, 1))
                elif change_var == 'fap_comput':
                    model = Model(N_cloud, N_FAP, N_user, cache_times=(1, 1, 1), comput_times=(1, temp[i], 1))
                elif change_var == 'user_comput':
                    model = Model(N_cloud, N_FAP, N_user, cache_times=(1, 1, 1), comput_times=(1, 1, temp[i]))
                else:
                    model = None
                # 博弈算法
                greedy = GreedyAlgorithm(model)
                greedy.solve()
                g_ans, g_cache, g_comput, g_arrive_loop, g_time = greedy.get_result()
                # 遗传算法
                queue = QueueAlgorithm(model)
                queue.solve()
                q_ans, q_cache, q_comput, q_time = queue.get_result()
                compare_g_ans[j + 1, i] = g_ans
                compare_g_time[j + 1, i] = g_time
                compare_q_ans[j + 1, i] = q_ans
                compare_q_time[j + 1, i] = q_time
                if abs(g_ans - q_ans) < 10 ** (-6):
                    same_ans_count += 1

            same_rate[1, i] = same_ans_count / N_test
            # 保存文件
            pd.DataFrame(compare_g_ans).to_csv(
                str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                change_var + str(begin) + 'to' + str(end) + 'g_ans' + '.csv',
                header=False, index=False)
            pd.DataFrame(compare_g_time).to_csv(
                str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                change_var + str(begin) + 'to' + str(end) + 'g_time' + '.csv',
                header=False, index=False)
            pd.DataFrame(compare_q_ans).to_csv(
                str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                change_var + str(begin) + 'to' + str(end) + 'q_ans' + '.csv',
                header=False, index=False)
            pd.DataFrame(compare_q_time).to_csv(
                str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                change_var + str(begin) + 'to' + str(end) + 'q_time' + '.csv',
                header=False, index=False)
            pd.DataFrame(same_rate).to_csv(
                str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                change_var + str(begin) + 'to' + str(end) + 'same_rate' + '.csv',
                header=False, index=False)

