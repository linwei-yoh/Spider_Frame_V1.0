#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'
from Task_Queue import TaskQueue
import queue
from enum import Enum


class ThreadSta(Enum):
    Init = 0  # 初始状态
    Work = 1  # 开始运行
    Finish = 2  # 线程结束
    Error = 3  # 线程报错


class SpiderManager(object):
    def __init__(self):
        self.Fetch_Sta = ThreadSta.Init  # 爬取线程状态
        self.Parse_Sta = ThreadSta.Init  # 解析线程状态
        self.Save_Sta = ThreadSta.Init  # 存储线程状态
        self.Clock_Sta = ThreadSta.Init  # 时钟线程状态
        self.TaskAllot_Sta = ThreadSta.Init  # 任务分配线程状态
        self.Monitor_Sta = ThreadSta.Init  # 监控线程状态

        self.fetch_queue = TaskQueue(queue.Queue())
        self.parse_queue = TaskQueue(queue.Queue())
        self.save_queue = TaskQueue(queue.Queue())

    def finish_all_threads(self):
        self.Fetch_Sta = ThreadSta.Finish  # 爬取线程状态
        self.Parse_Sta = ThreadSta.Finish  # 解析线程状态
        self.Save_Sta = ThreadSta.Finish  # 存储线程状态
        self.Clock_Sta = ThreadSta.Finish  # 时钟线程状态
        self.TaskAllot_Sta = ThreadSta.Finish  # 任务分配线程状态
        self.Monitor_Sta = ThreadSta.Finish  # 监控线程状态

    def show_all_sta(self):
        for sta in [self.Fetch_Sta, self.Parse_Sta, self.Save_Sta, self.Clock_Sta, self.TaskAllot_Sta,
                    self.Monitor_Sta]:
            print(type(sta), sta)

    def check_thread_error(self):
        for sta in [self.Fetch_Sta, self.Parse_Sta, self.Save_Sta, self.Clock_Sta, self.TaskAllot_Sta,
                    self.Monitor_Sta]:
            if sta == ThreadSta.Error:
                return True
        return False


if __name__ == '__main__':
    spiderMan = SpiderManager()
    spiderMan.show_all_sta()
    print("----------------------------------")
    spiderMan.finish_all_threads()
    spiderMan.show_all_sta()
    pass
