import geatpy as ea  # import geatpy
import numpy as np

from problem import MyProblem  # 导入自定义问题接口

if __name__ == '__main__':
    """===============================实例化问题对象==========================="""
    problem = MyProblem()  # 生成问题对象
    """=================================种群设置=============================="""
    Encoding = 'RI'  # 编码方式 实整数编码
    # 单种群
    # NIND = 1000  # 种群规模
    # Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    # population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    NIND = 10000  # 总种群规模
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
    myAlgorithm.MAXGEN = 100  # 最大进化代数
    myAlgorithm.trappedValue = 1e-6  # “进化停滞”判断阈值
    myAlgorithm.maxTrappedCount = 100  # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
    myAlgorithm.logTras = 1  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """===========================根据先验知识创建先知种群========================"""
    prophetPop = [None] * N_population
    prophetChrom = np.zeros(
        [1, problem.model.N_device * problem.model.N_task * 2])  # 假设已知[0,....,0]为一条比较优秀的染色体,也就为全部缓存和计算位置都在cloud上
    for i in range(N_population):
        prophetPop[i] = ea.Population(Encoding, Field, 1, prophetChrom)  # 实例化种群对象（设置个体数为1）
        myAlgorithm.call_aimFunc(prophetPop[i])  # 计算先知种群的目标函数值及约束（假如有约束）


    """==========================调用算法模板进行种群进化========================"""
    [BestIndi, population] = myAlgorithm.run(prophetPop)  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()  # 把最优个体的信息保存到文件中
    """=================================输出结果=============================="""
    print('评价次数：%s' % myAlgorithm.evalsNum)
    print('时间已过 %s 秒' % myAlgorithm.passTime)
    if BestIndi.sizes != 0:
        print('最优的目标函数值为：%s' % BestIndi.ObjV[0][0])
        print('最优的控制变量值为：')
        # for i in range(BestIndi.Phen.shape[1]):
        #     print(BestIndi.Phen[0, i])
    else:
        print('没找到可行解。')
