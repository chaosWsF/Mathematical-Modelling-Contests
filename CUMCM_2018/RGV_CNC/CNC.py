import numpy as np


class CNC:
    def __init__(self, code):
        self.code_num = code    # 编号
        self.switcher = 'empty'    # CNC空
        self.method_timer = 0   # CNC 计时器
        self.error_timer = 0

    def call_rgv(self):
        """请求上料，并返回CNC当前状态"""
        return self.code_num, self.switcher

    def processing(self, timer, t4, case3=False):
        """加工原料，并返回是否故障True/False"""
        self.switcher = 'open'  # 加工中

        self.method_timer += timer      # 更新计时器
        if self.method_timer >= t4:
            self.switcher = 'off'    # 加工完成
            self.method_timer = 0   # 计时器归零

        if case3:   # Case3中带有随机性的状况
            if np.random.choice([0, 1], p=[0.01, 0.99]) == 0:   # 出故障
                self.switcher = 'error'     # CNC故障
                self.method_timer = 0
                return True
            else:
                return False

    def error_repairing(self, timer, repairing_time):
        """修理故障的CNC"""
        self.error_timer += timer
        if self.error_timer >= repairing_time:
            self.switcher = 'empty'     # 故障修理完成，CNC重置为空
            self.error_timer = 0
