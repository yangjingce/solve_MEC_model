import geatpy as ea  # import geatpy
import numpy as np
from Model import Model
from queue_problem import MyProblem  # 导入自定义问题接口
from Decision import Decision

if __name__ == '__main__':
    """===============================实例化问题对象==========================="""
    problem = MyProblem()  # 生成问题对象
    """=================================种群设置=============================="""
    Encoding = 'P'  # 编码方式 排列编码
    # 单种群
    # NIND = 1000  # 种群规模
    # Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    # population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    NIND = 100 # 总种群规模
    N_population = 4 # 种群数
    NINDs = [NIND // N_population] * N_population  # 种群规模
    population = [None] * N_population # 创建种群列表
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    for i in range(N_population):

        population[i] = ea.Population(Encoding, Field, NINDs[i])  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    # myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象
    # myAlgorithm.recOper.XOVR = 0.7  # 交叉概率
    # myAlgorithm.mutOper.Pm = 1  # 变异概率

    myAlgorithm = ea.soea_multi_SEGA_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 5  # 最大进化代数
    myAlgorithm.trappedValue = 1e-6  # “进化停滞”判断阈值
    myAlgorithm.maxTrappedCount = 10000  # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
    myAlgorithm.logTras = 1  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）



    """==========================调用算法模板进行种群进化========================"""
    [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群，不使用先知种群
    #[BestIndi, population] = myAlgorithm.run(prophetPop)  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save('order')  # 把最优个体的信息保存到文件中
    """=================================输出结果=============================="""
    print('评价次数：%s' % myAlgorithm.evalsNum)
    print('时间已过 %s 秒' % myAlgorithm.passTime)
    if BestIndi.sizes != 0:
        print('最优的目标函数值为：%s' % BestIndi.ObjV[0][0])
        print('最优的控制变量值为：')
        for i in range(BestIndi.Phen.shape[1]):
            print(BestIndi.Phen[0, i])
    else:
        print('没找到可行解。')

    def convert_result(order_ans):

        model = Model()
        # 初始化决策对象
        decision = Decision(model.N_cloud, model.N_FAP, model.N_user, model.N_task, model.device_cache,
                            model.device_comput,
                            model.task_cache, model.task_comput)
        # decision.set_delay(model.delay)
        decision.set_bandwidth(model.bandwidth)
        decision.set_possible(model.possible)
        # 初始解，所有缓存和计算在云端位置上
        decision.cache_position = np.zeros([model.N_device, model.N_task])
        decision.comput_position = np.zeros([model.N_device, model.N_task])
        # 按step步骤优化解
        for step in order_ans:
            step_user = step // model.N_task + model.N_cloud + model.N_FAP
            step_task = step % model.N_task
            decision.optimize_device_task_time(step_user, step_task,decision.get_single_device_time)
        # 计算延迟
        decision.set_device_time()
        return decision
    result = convert_result(BestIndi.Phen[0])
    print('------------------------------')
    print(result.get_max_device_time())
    print(result.cache_position)
    print(result.comput_position)


