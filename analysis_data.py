import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    def analysis_data(change_var, change_begin, change_end, N_cloud=1, N_FAP=10, N_user=25, N_test=1):
        if change_var == 'user':
            # 改变终端用户的数量
            # 读取数据
            g_ans = np.loadtxt(change_var + '/' + '1_10_10to70g_ans.csv', delimiter=',')
            g_time = np.loadtxt(change_var + '/' + '1_10_10to70g_time.csv', delimiter=',')
            q_ans = np.loadtxt(change_var + '/' + '1_10_10to70q_ans.csv', delimiter=',')
            q_time = np.loadtxt(change_var + '/' + '1_10_10to70q_time.csv', delimiter=',')
            # 数据处理
            user_range = g_ans[0, :]
            g_ans = g_ans[1:, :]
            g_time = g_time[1:, :]
            q_ans = q_ans[1:, :]
            q_time = q_time[1:, :]
            # 求平均
            average_g_ans = np.mean(g_ans, axis=0)
            average_g_time = np.mean(g_time, axis=0)
            average_q_ans = np.mean(q_ans, axis=0)
            average_q_time = np.mean(q_time, axis=0)
            # 求方差
            var_delay = np.var(g_ans, axis=0, ddof=1)
            # 绘图
            plt.figure()
            # plt.plot(user_range, average_g_ans, color='r', marker='o', linestyle='dashed', label='g_ans')
            plt.plot(user_range, average_g_ans, marker='o', label='g_ans')
            plt.plot(user_range, var_delay, marker='*', label='var')
            plt.legend(loc='upper left')
            plt.xlabel('end users\' Number')
            plt.ylabel('delay(s)')
            plt.title('delay versus end users\' number')
            plt.show()
            plt.figure()
            plt.plot(user_range, average_q_time, marker='s', label='genetic algorithm based approach')
            plt.plot(user_range, average_g_time / 8, marker='^', label='game-based approach')

            plt.legend(loc='upper left')
            plt.xlabel('The number of end users')
            plt.ylabel('Run time (s)')
            # plt.title('spend time versus end users\' number')
            plt.show()
        elif change_var == 'fap':
            # 改变fap的数量
            # 读取数据
            g_ans = np.loadtxt(change_var + '/' + '1_3to25_25g_ans.csv', delimiter=',')
            g_time = np.loadtxt(change_var + '/' + '1_3to25_25g_time.csv', delimiter=',')
            q_ans = np.loadtxt(change_var + '/' + '1_3to25_25q_ans.csv', delimiter=',')
            q_time = np.loadtxt(change_var + '/' + '1_3to25_25q_time.csv', delimiter=',')
            # 数据处理
            user_range = g_ans[0, :]
            g_ans = g_ans[1:, :]
            g_time = g_time[1:, :]
            q_ans = q_ans[1:, :]
            q_time = q_time[1:, :]
            # 求平均
            average_g_ans = np.mean(g_ans, axis=0)
            average_g_time = np.mean(g_time, axis=0)
            average_q_ans = np.mean(q_ans, axis=0)
            average_q_time = np.mean(q_time, axis=0)
            # 求方差
            var_delay = np.var(g_ans, axis=0, ddof=1)
            # 绘图
            plt.figure()
            # plt.plot(user_range, average_g_ans, color='r', marker='o', linestyle='dashed', label='g_ans')
            plt.plot(user_range, average_g_ans, marker='o', label='g_ans')
            plt.plot(user_range, var_delay, marker='*', label='var')
            plt.legend(loc='upper left')
            plt.xlabel('F-APs\' Number')
            plt.ylabel('delay(s)')
            plt.title('delay versus F-APs\' number')
            plt.show()
            plt.figure()
            plt.plot(user_range, average_q_time, marker='s', label='genetic algorithm based approach')
            plt.plot(user_range, average_g_time / 8, marker='^', label='game-based approach')
            plt.legend(loc='upper left')
            plt.xlabel('The number of F-APs')
            plt.ylabel('Run time (s)')
            plt.title('spend time versus F-APs\' number')
            plt.show()
        else:
            begin = change_begin
            end = change_end
            file_name_prefix = change_var + '/' + str(N_cloud) + '_' + str(N_FAP) + '_' + str(
                N_user) + change_var + str(begin) + 'to' + str(
                end)
            # 读取数据
            g_ans = np.loadtxt(file_name_prefix + 'g_ans.csv', delimiter=',')
            g_time = np.loadtxt(file_name_prefix + 'g_time.csv', delimiter=',')
            q_ans = np.loadtxt(file_name_prefix + 'q_ans.csv', delimiter=',')
            q_time = np.loadtxt(file_name_prefix + 'q_time.csv', delimiter=',')
            # 数据处理
            user_range = g_ans[0, :]
            g_ans = g_ans[1:, :]
            g_time = g_time[1:, :]
            q_ans = q_ans[1:, :]
            q_time = q_time[1:, :]
            # 求平均
            average_g_ans = np.mean(g_ans, axis=0)
            average_g_time = np.mean(g_time, axis=0)
            average_q_ans = np.mean(q_ans, axis=0)
            average_q_time = np.mean(q_time, axis=0)
            # # 求方差
            # var_delay = np.var(g_ans, axis=0, ddof=1)
            # 绘图
            # plt.figure()
            # # plt.plot(user_range, average_g_ans, color='r', marker='o', linestyle='dashed', label='g_ans')
            # plt.plot(user_range, average_g_ans, marker='o', label='g_ans')
            # # plt.plot(user_range, g_ans, marker='o', label='g_ans')
            # # plt.plot(user_range, var_delay, marker='*', label='var')
            # # plt.plot(user_range, average_q_ans, marker='v', label='q_ans')
            # # plt.plot(user_range, q_ans, marker='v', label='q_ans')
            # plt.legend(loc='upper left')
            # plt.xlabel(change_var)
            # plt.ylabel('delay(s)')
            # plt.title('delay versus ' + change_var + '\' number')
            # plt.show()
            if change_var == 'user_comput':
                plt.figure()
                plt.plot(user_range * 5, average_q_ans, marker='v', label='genetic algorithm based approach')
                plt.plot(user_range * 5, average_g_ans, marker='o', label='game-based approach')
                plt.legend(loc='upper right')
                plt.xlabel('End users\' computation capability (TFLOPs)')
                plt.ylabel('Delay(s)')
                plt.show()
            elif change_var == 'fap_comput':
                plt.figure()
                plt.plot(user_range * 130, average_q_ans, marker='v', label='genetic algorithm based approach')
                plt.plot(user_range * 130, average_g_ans, marker='o', label='game-based approach')
                plt.legend(loc='upper right')
                plt.xlabel('F-APs\' computation capability (TFLOPs)')
                plt.ylabel('Delay(s)')
                plt.show()
            elif change_var == 'cloud_comput':
                plt.figure()
                plt.plot(user_range * 2000, average_q_ans, marker='v', label='genetic algorithm based approach')
                plt.plot(user_range * 2000, average_g_ans, marker='o', label='game-based approach')
                plt.legend(loc='upper right')
                plt.xlabel('Cloud\'s computation capability (TFLOPs)')
                plt.ylabel('Delay(s)')
                plt.show()
            elif change_var == 'user_cache':
                plt.figure()
                plt.plot(user_range * 5, average_q_ans, marker='v', label='genetic algorithm based approach')
                plt.plot(user_range * 5, average_g_ans, marker='o', label='game-based approach')
                plt.legend(loc='upper right')
                plt.xlabel('End users\' cache (MB)')
                plt.ylabel('Delay(s)')
                plt.show()
            elif change_var == 'fap_cache':
                plt.figure()
                plt.plot(user_range * 30, average_q_ans, marker='v', label='genetic algorithm based approach')
                plt.plot(user_range * 30, average_g_ans, marker='o', label='game-based approach')
                plt.legend(loc='upper right')
                plt.xlabel('F-APs\' cache (MB)')
                plt.ylabel('Delay(s)')
                plt.show()

    change_var_list = ['user', 'fap', 'cloud_cache', 'fap_cache', 'user_cache', 'cloud_comput', 'fap_comput',
                       'user_comput']
    analysis_data(change_var_list[6], 0.5, 5)
