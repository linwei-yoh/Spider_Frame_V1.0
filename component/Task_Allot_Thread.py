#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import time
from threading import Thread
from Schedule import Schedule
from logger_config import report_logger
from Spider_Manager import ThreadSta


# 低内聚
class TaskAllot(Thread):
    def __init__(self, client, schedule: Schedule, spiderManager):
        """
        定期检查任务队列的内容量，如果消耗完则从数据来源client 压入schedule中frequency量的任务
        :param client: 数据来源
        :param spiderManager: 爬虫管理
        :param schedule: 调度参数表
        """
        Thread.__init__(self, name='task_allot', daemon=True)
        self.client = client
        self.spiderManager = spiderManager
        self.schedule = schedule

    def run(self):
        self.spiderManager.TaskAllot_Sta = ThreadSta.Work
        try:
            self._run()
        except Exception:
            report_logger.error("TaskAllotThread 出错")
            self.spiderManager.fetch_queue.is_valid = False
            self.spiderManager.TaskAllot_Sta = ThreadSta.Error

    def _run(self):
        while True:
            if self.spiderManager.fetch_queue.is_valid:
                rec, fin = self.spiderManager.fetch_queue.get_count()
                if self.schedule.frequency > (rec - fin):
                    need = self.schedule.frequency - (rec - fin)
                    for url, keys in self.client.get_idle_task(need):
                        self.spiderManager.fetch_queue.put_nowait([url, keys, 0, 0])
            time.sleep(self.schedule.interval)

            if self.spiderManager.TaskAllot_Sta == ThreadSta.Finish:
                break



if __name__ == '__main__':
    pass
