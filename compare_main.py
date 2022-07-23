from Model import Model
from Greedy_algorithm_main import GreedyAlgorithm
from queue_main import QueueAlgorithm
import numpy as np
import pandas as pd
from pylab import *
from Device import Device
from Decision import Decision


def both_solve(m):
    # 博弈算法
    g = GreedyAlgorithm(m)
    g.solve()
    g_ans, g_cache, g_comput, g_arrive_loop, g_time = g.get_result()
    # 遗传算法
    q = QueueAlgorithm(m)
    q.solve()
    q_ans, q_cache, q_comput, q_time = q.get_result()

    same = 1 if abs(g_ans - q_ans) < 10 ** (-6) else 0
    return g_ans, g_time, q_ans, q_time, same


def generate_data(change_var, change_begin, change_end, N_cloud=1, N_FAP=10, N_user=25, N_test=1):
    if change_var == 'user':
        # 改变用户数
        begin_user = change_begin
        end_user = change_end
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
            pd.DataFrame(compare_user_g_ans).to_csv(change_var + '/' +
                                                    str(N_cloud) + '_' + str(N_FAP) + '_' + str(
                begin_user) + 'to' + str(end_user) + 'g_ans' + '.csv',
                                                    header=False, index=False)
            pd.DataFrame(compare_user_g_time).to_csv(change_var + '/' +
                                                     str(N_cloud) + '_' + str(N_FAP) + '_' + str(
                begin_user) + 'to' + str(end_user) + 'g_time' + '.csv',
                                                     header=False, index=False)
            pd.DataFrame(compare_user_q_ans).to_csv(change_var + '/' +
                                                    str(N_cloud) + '_' + str(N_FAP) + '_' + str(
                begin_user) + 'to' + str(end_user) + 'q_ans' + '.csv',
                                                    header=False, index=False)
            pd.DataFrame(compare_user_q_time).to_csv(change_var + '/' +
                                                     str(N_cloud) + '_' + str(N_FAP) + '_' + str(
                begin_user) + 'to' + str(end_user) + 'q_time' + '.csv',
                                                     header=False, index=False)
            pd.DataFrame(same_rate).to_csv(change_var + '/' +
                                           str(N_cloud) + '_' + str(N_FAP) + '_' + str(begin_user) + 'to' + str(
                end_user)
                                           + 'same_rate' + '.csv',
                                           header=False, index=False)
    elif change_var == 'fap':
        # 改变的fap数
        begin_fap = change_begin
        end_fap = change_end
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
            pd.DataFrame(compare_fap_g_ans).to_csv(change_var + '/' +
                                                   str(N_cloud) + '_' + str(begin_fap) + 'to' + str(
                end_fap) + '_' + str(N_user) + 'g_ans' + '.csv',
                                                   header=False, index=False)
            pd.DataFrame(compare_fap_g_time).to_csv(change_var + '/' +
                                                    str(N_cloud) + '_' + str(begin_fap) + 'to' + str(
                end_fap) + '_' + str(N_user) + 'g_time' + '.csv',
                                                    header=False, index=False)
            pd.DataFrame(compare_fap_q_ans).to_csv(change_var + '/' +
                                                   str(N_cloud) + '_' + str(begin_fap) + 'to' + str(
                end_fap) + '_' + str(N_user) + 'q_ans' + '.csv',
                                                   header=False, index=False)
            pd.DataFrame(compare_fap_q_time).to_csv(change_var + '/' +
                                                    str(N_cloud) + '_' + str(begin_fap) + 'to' + str(
                end_fap) + '_' + str(N_user) + 'q_time' + '.csv',
                                                    header=False, index=False)
            pd.DataFrame(same_rate).to_csv(
                change_var + '/' + str(N_cloud) + '_' + str(begin_fap) + 'to' + str(end_fap) + '_' + str(N_user)
                + 'same_rate' + '.csv',
                header=False, index=False)

    elif change_var == 'multi':
        multiple_list = np.linspace(change_begin, change_end, 20)
        # 设备的基准能力
        cloud_cache, fap_cache, user_cache, cloud_comput, fap_comput, user_comput = 1000, 30, 5, 2000, 130, 5
        # 先生成N_test个模型
        model_list = [Model(N_cloud, N_FAP, N_user) for _ in range(N_test)]
        # var_l = ['cloud_comput']
        var_l = ['fap_cache', 'user_cache', 'cloud_comput', 'fap_comput']
        for v, vvv in enumerate(var_l):
            compare_g_ans = np.zeros([N_test + 1, len(multiple_list)])
            compare_g_time = np.zeros([N_test + 1, len(multiple_list)])
            compare_q_ans = np.zeros([N_test + 1, len(multiple_list)])
            compare_q_time = np.zeros([N_test + 1, len(multiple_list)])
            # 变化轴
            compare_g_ans[0, :] = multiple_list.T
            compare_g_time[0, :] = multiple_list.T
            compare_q_ans[0, :] = multiple_list.T
            compare_q_time[0, :] = multiple_list.T
            # 遍历模型和倍数求解
            for j, model in enumerate(model_list):
                for q, multiple in enumerate(multiple_list):
                    print('----------',vvv,'---------',j,'----------',q,'----------')
                    if v == 0:
                        device = Device(model.N_cloud, model.N_FAP,
                                        model.N_user, model, cloud_cache,
                                        fap_cache * multiple, user_cache, cloud_comput, fap_comput, user_comput)
                    elif v == 1:
                        device = Device(model.N_cloud, model.N_FAP,
                                        model.N_user, model.N_task, cloud_cache, fap_cache,
                                        user_cache * multiple, cloud_comput, fap_comput, user_comput)
                    elif v == 2:
                        device = Device(model.N_cloud, model.N_FAP,
                                        model.N_user, model.N_task, cloud_cache, fap_cache,
                                        user_cache, cloud_comput * multiple, fap_comput, user_comput)
                    else:
                        device = Device(model.N_cloud, model.N_FAP,
                                        model.N_user, model.N_task, cloud_cache, fap_cache,
                                        user_cache, cloud_comput, fap_comput * multiple, user_comput)
                    device.set_all()
                    model.device_cache = device.device_cache  # 设备的缓存能力
                    model.device_comput = device.device_comput  # 设备的计算能力
                    compare_g_ans[j + 1, q], compare_g_time[j + 1, q], compare_q_ans[j + 1, q], compare_q_time[
                        j + 1, q], same_ans_count = both_solve(model)

            # 保存文件
            pre_road = vvv + '/' + str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) + vvv + str(
                change_begin) + 'to' + str(change_end)
            pd.DataFrame(compare_g_ans).to_csv(pre_road + 'g_ans' + '.csv',
                                               header=False, index=False)
            pd.DataFrame(compare_g_time).to_csv(pre_road + 'g_time' + '.csv',
                                                header=False, index=False)
            pd.DataFrame(compare_q_ans).to_csv(pre_road + 'q_ans' + '.csv',
                                               header=False, index=False)
            pd.DataFrame(compare_q_time).to_csv(pre_road + 'q_time' + '.csv',
                                                header=False, index=False)

        # 全部任务卸载到云端
        ans = np.zeros([N_test + 1, len(multiple_list)])
        ans[0, :] = multiple_list.T
        for j, model in enumerate(model_list):
            for q, multiple in enumerate(multiple_list):
                device = Device(model.N_cloud, model.N_FAP, model.N_user, model, cloud_cache, fap_cache, user_cache,
                                cloud_comput * multiple, fap_comput, user_comput)
                device.set_all()
                model.device_cache = device.device_cache  # 设备的缓存能力
                model.device_comput = device.device_comput  # 设备的计算能力
                # 初始化决策对象
                decision = Decision(model.N_cloud, model.N_FAP, model.N_user, model.N_task,
                                    model.device_cache,
                                    model.device_comput, model.task_cache, model.task_comput)
                decision.set_bandwidth(model.bandwidth)
                decision.set_possible(model.possible)
                # 设置初始解，所有缓存和计算在云端位置上
                decision.set_cache_position(np.zeros([model.N_device, model.N_task]))
                decision.set_comput_position(np.zeros([model.N_device, model.N_task]))
                decision.set_device_time()
                ans[j + 1, q] = np.max(decision.every_device_time)
        # 保存
        pd.DataFrame(ans).to_csv('all_cloud.csv', header=False, index=False)

    elif change_var == 'three_compare':
        multiple_list = np.linspace(change_begin, change_end, 5)
        # 设备的基准能力
        cloud_cache, fap_cache, user_cache, cloud_comput, fap_comput, user_comput = 1000, 30, 5, 2000, 130, 5
        # 先生成N_test个模型
        model_list = [Model(N_cloud, N_FAP, N_user) for _ in range(N_test)]
        compare_g_ans = np.zeros([N_test + 1, len(multiple_list)])
        compare_g_time = np.zeros([N_test + 1, len(multiple_list)])
        compare_q_ans = np.zeros([N_test + 1, len(multiple_list)])
        compare_q_time = np.zeros([N_test + 1, len(multiple_list)])
        # 变化轴
        compare_g_ans[0, :] = multiple_list.T
        compare_g_time[0, :] = multiple_list.T
        compare_q_ans[0, :] = multiple_list.T
        compare_q_time[0, :] = multiple_list.T

        # 全部任务卸载到云端
        ans = np.zeros([N_test + 1, len(multiple_list)])
        ans[0, :] = multiple_list.T

        # 遍历模型和倍数求解
        for j, model in enumerate(model_list):
            for q, multiple in enumerate(multiple_list):
                device = Device(model.N_cloud, model.N_FAP,
                                model.N_user, model.N_task, cloud_cache, fap_cache,
                                user_cache, cloud_comput * multiple, fap_comput, user_comput)
                device.set_all()
                model.device_cache = device.device_cache  # 设备的缓存能力
                model.device_comput = device.device_comput  # 设备的计算能力
                # 两种算法计算
                compare_g_ans[j + 1, q], compare_g_time[j + 1, q], compare_q_ans[j + 1, q], compare_q_time[
                    j + 1, q], same_ans_count = both_solve(model)

                # 初始化决策对象
                decision = Decision(model.N_cloud, model.N_FAP, model.N_user, model.N_task,
                                    model.device_cache,
                                    model.device_comput, model.task_cache, model.task_comput)
                decision.set_bandwidth(model.bandwidth)
                decision.set_possible(model.possible)
                # 设置初始解，所有缓存和计算在云端位置上
                decision.set_cache_position(np.zeros([model.N_device, model.N_task]))
                decision.set_comput_position(np.zeros([model.N_device, model.N_task]))
                decision.set_device_time()
                ans[j + 1, q] = np.max(decision.every_device_time)

        # 保存文件
        pre_road = 'cloud_comput' + '/' + str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) + 'cloud_comput' + str(
            change_begin) + 'to' + str(change_end)
        pd.DataFrame(compare_g_ans).to_csv(pre_road + 'g_ans' + '.csv',
                                           header=False, index=False)
        pd.DataFrame(compare_g_time).to_csv(pre_road + 'g_time' + '.csv',
                                            header=False, index=False)
        pd.DataFrame(compare_q_ans).to_csv(pre_road + 'q_ans' + '.csv',
                                           header=False, index=False)
        pd.DataFrame(compare_q_time).to_csv(pre_road + 'q_time' + '.csv',
                                            header=False, index=False)
        # 保存
        pd.DataFrame(ans).to_csv('all_cloud.csv', header=False, index=False)





    else:
        # 改变能力
        begin = change_begin
        end = change_end
        multiple_list = np.linspace(begin, end, 5)

        compare_g_ans = np.zeros([N_test + 1, len(multiple_list)])
        compare_g_time = np.zeros([N_test + 1, len(multiple_list)])
        compare_q_ans = np.zeros([N_test + 1, len(multiple_list)])
        compare_q_time = np.zeros([N_test + 1, len(multiple_list)])
        same_rate = np.zeros([2, len(multiple_list)])
        # 先生成N_test个模型
        model_list = [Model(N_cloud, N_FAP, N_user) for _ in range(N_test)]

        for i in range(len(multiple_list)):
            same_ans_count = 0
            compare_g_ans[0, i] = multiple_list[i]
            compare_g_time[0, i] = multiple_list[i]
            compare_q_ans[0, i] = multiple_list[i]
            compare_q_time[0, i] = multiple_list[i]
            same_rate[0, i] = multiple_list[i]
            for j in range(N_test):
                print('----------', multiple_list[i], '----------', j, '------------')
                # 设备的基准能力
                cloud_cache, fap_cache, user_cache, cloud_comput, fap_comput, user_comput = 1000, 30, 5, 2000, 130, 5
                # 改变设备的能力
                model = model_list[j]
                # 生成新的设备能力
                if change_var == 'cloud_cache':
                    device = Device(model.N_cloud, model.N_FAP, model.N_user, model.N_task,
                                    cloud_cache * multiple_list[i],
                                    fap_cache, user_cache, cloud_comput, fap_comput, user_comput)
                elif change_var == 'fap_cache':
                    device = Device(model.N_cloud, model.N_FAP, model.N_user, model.N_task, cloud_cache,
                                    fap_cache * multiple_list[i], user_cache, cloud_comput, fap_comput, user_comput)
                elif change_var == 'user_cache':
                    device = Device(model.N_cloud, model.N_FAP, model.N_user, model.N_task, cloud_cache, fap_cache,
                                    user_cache * multiple_list[i], cloud_comput, fap_comput, user_comput)
                elif change_var == 'cloud_comput':
                    device = Device(model.N_cloud, model.N_FAP, model.N_user, model.N_task, cloud_cache, fap_cache,
                                    user_cache, cloud_comput * multiple_list[i], fap_comput, user_comput)
                elif change_var == 'fap_comput':
                    device = Device(model.N_cloud, model.N_FAP, model.N_user, model.N_task, cloud_cache, fap_cache,
                                    user_cache, cloud_comput, fap_comput * multiple_list[i], user_comput)
                elif change_var == 'user_comput':
                    device = Device(model.N_cloud, model.N_FAP, model.N_user, model.N_task, cloud_cache, fap_cache,
                                    user_cache, cloud_comput, fap_comput, user_comput * multiple_list[i])
                else:
                    pass

                device.set_all()
                model.device_cache = device.device_cache  # 设备的缓存能力
                model.device_comput = device.device_comput  # 设备的计算能力
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
            pd.DataFrame(compare_g_ans).to_csv(change_var + '/' +
                                               str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                                               change_var + str(begin) + 'to' + str(end) + 'g_ans' + '.csv',
                                               header=False, index=False)
            pd.DataFrame(compare_g_time).to_csv(change_var + '/' +
                                                str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                                                change_var + str(begin) + 'to' + str(end) + 'g_time' + '.csv',
                                                header=False, index=False)
            pd.DataFrame(compare_q_ans).to_csv(change_var + '/' +
                                               str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                                               change_var + str(begin) + 'to' + str(end) + 'q_ans' + '.csv',
                                               header=False, index=False)
            pd.DataFrame(compare_q_time).to_csv(change_var + '/' +
                                                str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                                                change_var + str(begin) + 'to' + str(end) + 'q_time' + '.csv',
                                                header=False, index=False)
            pd.DataFrame(same_rate).to_csv(change_var + '/' +
                                           str(N_cloud) + '_' + str(N_FAP) + '_' + str(N_user) +
                                           change_var + str(begin) + 'to' + str(end) + 'same_rate' + '.csv',
                                           header=False, index=False)


if __name__ == '__main__':

    # change_var_list = ['user', 'fap', 'cloud_cache', 'fap_cache', 'user_cache', 'cloud_comput', 'fap_comput',
    #                    'user_comput']
    # for i in range(3, 7):
    #     generate_data(change_var_list[i], 0.5, 5, N_test=5)
    generate_data('multi', 0.5, 5, N_test=5)
