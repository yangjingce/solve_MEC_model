from Model import Model
from Greedy_algorithm_main import GreedyAlgorithm
from queue_main import QueueAlgorithm
import numpy as np
import pandas as pd
from pylab import *

if __name__ == '__main__':
    compare_user_g_ans = np.zeros([3, 5])
    pd.DataFrame(compare_user_g_ans).to_csv(
        'user/test' + '.csv',
        header=False, index=False)
