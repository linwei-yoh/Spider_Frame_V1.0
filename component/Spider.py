#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'
import time


from Schedule import Schedule
from Clock_Thread import ClockThread
from Task_Allot_Thread import TaskAllot
from Fetch_Thread import FetchThread
from Parse_Thread import ParseThread
from Save_Thread import SaveThread
from Monitor_Thread import MonitorThread
from Spider_Manager import SpiderManager


class Spider(object):
    def __init__(self, fetch_worker, parse_worker, save_worker, schedule: Schedule, client=None):
        """
        爬虫组件初始化
        :param fetch_worker: 爬取处理组件
        :param parse_worker: 解析处理组件
        :param save_worker: 存储处理组件
        :param schedule: 调度参数组件
        :param client: 爬取任务来源 
        """
        self.client = client

        self.fetcher = fetch_worker
        self.parser = parse_worker
        self.saver = save_worker

        self.schedule = schedule
        self.spiderManager = SpiderManager()

    def start_work_and_wait_done(self, fetcher_num=10, parser_num=1, monitor_time=5):
        """
        开启爬取
        :param fetcher_num: 爬取线程数
        :param parser_num:  解析进程数
        :param montion_time: 监视线程报告间隔
        """
        # 时钟线程
        clock_thread = ClockThread(self.schedule,self.spiderManager)
        # 监视线程
        monitor_thread = MonitorThread(self.spiderManager, sleeptime=monitor_time)

        # 任务调度线程
        task_allot_thread = TaskAllot(self.client, self.schedule, self.spiderManager)
        # 爬取线程
        fetch_thread = FetchThread(self.fetcher, fetcher_num, self.spiderManager)
        # 解析线程
        parse_thread = ParseThread(self.parser, parser_num, self.spiderManager)
        # 存储线程
        save_thread = SaveThread(self.saver, self.spiderManager)

        for thread in [clock_thread, task_allot_thread, fetch_thread, parse_thread, save_thread, monitor_thread]:
            thread.start()

        while True:
            if self.is_all_task_done() or self.spiderManager.check_thread_error():
                self.spiderManager.finish_all_threads()
                break
            time.sleep(1)

        for thread in [fetch_thread, parse_thread, save_thread, monitor_thread]:
            thread.join()

    def set_start_url(self, url, keys=None):
        if self.client is None:
            self.spiderManager.fetch_queue.put_nowait([url, keys])
        else:
            self.client.add_idle_task(url, keys)

    def is_all_task_done(self):
        if not self.spiderManager.fetch_queue.is_valid:
            if self.spiderManager.parse_queue.is_counter_equal() and \
                    self.spiderManager.save_queue.is_counter_equal():
                return True
            else:
                return False
        else:
            if self.client.get_idle_tasks_size() == 0 and \
                    self.spiderManager.fetch_queue.is_counter_equal() and \
                    self.spiderManager.parse_queue.is_counter_equal() and \
                    self.spiderManager.save_queue.is_counter_equal():
                return True
            else:
                return False
        pass


if __name__ == '__main__':
    pass
