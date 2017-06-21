#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from dateutil.parser import parse


class Schedule(object):
    def __init__(self, start, end, fast_fqy: int, nor_fqy: int, interval: int = 1):
        """
        任务调度配置模块
        :param start: 快速区间起始时间
        :param end: 快速区间结束时间
        :param fast_fqy: 快速爬取频率
        :param nor_fqy: 慢速爬取频率
        :param interval: 压入任务检查周期
        """
        self.start = start
        self.end = end
        self.fast = int(fast_fqy)
        self.slow = int(nor_fqy)
        self.over_night = True if parse(start) > parse(end) else False
        self.frequency = self.slow
        self.interval = interval if interval > 0 else 1

    def fcy_turn_fast(self):
        self.frequency = self.fast
        print("快速状态:%d / %ds" % (self.frequency, self.interval))

    def fcy_turn_slow(self):
        self.frequency = self.slow
        print("常规状态:%d / %ds" % (self.frequency, self.interval))


if __name__ == '__main__':
    pass
