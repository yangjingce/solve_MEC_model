import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # 读取数据
    g_ans = np.loadtxt('1_10_10to70g_ans.csv', delimiter=',')
    g_time = np.loadtxt('1_10_10to70g_time.csv', delimiter=',')
    q_ans = np.loadtxt('1_10_10to70q_ans.csv', delimiter=',')
    q_time = np.loadtxt('1_10_10to70q_time.csv', delimiter=',')
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
    # 绘图
    plt.figure()
    plt.plot(user_range, average_g_ans, label='g_ans')
    plt.show()
    plt.figure()
    plt.plot(user_range, average_g_time, label='g_time')
    plt.plot(user_range, average_q_time, label='q_time')
    plt.legend(loc='upper left')
    plt.show()
