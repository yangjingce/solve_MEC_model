import numpy as np


class Device:
    def __init__(self, N_cloud, N_FAP, N_user, N_task, cloud_cache=100000, FAP_cache=110, user_cache=10,
                 cloud_comput=100000, FAP_comput=110,
                 user_comput=10):
    # def __init__(self, N_cloud, N_FAP, N_user, N_task, cloud_cache=100000, FAP_cache=1000, user_cache=1000,
    #              cloud_comput=100000, FAP_comput=1000,
    #              user_comput=1000):
        self.N_cloud = N_cloud
        self.N_FAP = N_FAP
        self.N_user = N_user
        self.cloud_cache = cloud_cache
        self.FAP_cache = FAP_cache
        self.user_cache = user_cache
        self.cloud_comput = cloud_comput
        self.FAP_comput = FAP_comput
        self.user_comput = user_comput
        self.N_device = self.N_cloud + self.N_FAP + self.N_user
        self.N_task = N_task
        self.cache = np.zeros([1, self.N_device])  # 任务缓存内容的大小
        self.comput = np.zeros([1, self.N_device])  # 任务计算内容的大小

    def set_cloud_cache(self):
        for device in range(self.N_cloud):
            self.cache[0, device] = self.cloud_cache
        return

    def set_FAP_cache(self):
        for device in range(self.N_cloud, self.N_cloud + self.N_FAP):
            self.cache[0, device] = self.FAP_cache
        return

    def set_user_cache(self):
        for device in range(self.N_cloud + self.N_FAP, self.N_device):
            self.cache[0, device] = self.user_cache
        return

    def set_cloud_comput(self):
        for device in range(self.N_cloud):
            self.comput[0, device] = self.cloud_comput
        return

    def set_FAP_comput(self):
        for device in range(self.N_cloud, self.N_cloud + self.N_FAP):
            self.comput[0, device] = self.FAP_comput
        return

    def set_user_comput(self):
        for device in range(self.N_cloud + self.N_FAP, self.N_device):
            self.comput[0, device] = self.user_comput
        return

    def set_all(self):
        self.set_cloud_cache()
        self.set_FAP_cache()
        self.set_user_cache()
        self.set_cloud_comput()
        self.set_FAP_comput()
        self.set_user_comput()


if __name__ == '__main__':
    a = Device(1, 3, 5, 10)
    a.set_all()
    print(a.cache)
    print(a.comput)
