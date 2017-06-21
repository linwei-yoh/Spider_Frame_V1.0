#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from threading import Thread
import queue

from Spider_Manager import ThreadSta
from logger_config import report_logger


class SaveWorker(object):
    """
    覆盖需要修改的方法
    """

    def __init__(self):
        pass

    def result_save(self, url, keys, item):
        result = item + " done"
        return result


class SaveThread(Thread):
    def __init__(self, worker, spiderManager):
        """
        存储线程
        :param worker: 存储任务处理类
        :param spiderManager: 爬虫管理
        """
        Thread.__init__(self, name='Saver')
        self.worker = worker
        self.spiderManager = spiderManager

    def run(self):
        self.spiderManager.Save_Sta = ThreadSta.Work
        try:
            self._run()
        except Exception as exc:
            report_logger.error("SaveThread ", exc)
            self.spiderManager.Save_Sta = ThreadSta.Error

    def _run(self):
        while True:
            try:
                url, keys, item = self.spiderManager.save_queue.get(block=True, timeout=5)
                self.worker.result_save(url, keys, item)
                self.spiderManager.save_queue.task_done()
            except queue.Empty:
                if self.spiderManager.Save_Sta == ThreadSta.Finish:
                    break


if __name__ == '__main__':
    pass
