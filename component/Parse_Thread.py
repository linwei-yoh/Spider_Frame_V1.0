#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from concurrent.futures import ProcessPoolExecutor
from threading import Thread
import queue

from Spider_Manager import ThreadSta
from logger_config import report_logger
from Task_Queue import TaskQueue
from functools import partial


class ParseWorker(object):
    """
    覆盖html_Parse方法
    """

    def __init__(self, max_deep=0):
        """
        :param max_deep: 最大爬取深度 0:无限制
        """
        self.max_deep = max_deep

    def html_parse(self, url, keys, deep, content):
        result = content + " done"
        return result


class ParseThread(Thread):
    def __init__(self, worker, num, spiderManager):
        """
        建立解析线程
        :param worker: 解析处理类
        :param num: 解析进程数量
        :param spiderManager: 爬虫管理
        """
        Thread.__init__(self, name='Parser')
        self.worker = worker
        self.num = num
        self.spiderManager = spiderManager

    def run(self):
        self.spiderManager.Parse_Sta = ThreadSta.Work
        try:
            self._run()
        except Exception as exc:
            report_logger.error("ParseThread ", exc)
            self.spiderManager.Parse_Sta = ThreadSta.Error

    def _run(self):
        with ProcessPoolExecutor(max_workers=self.num) as executor:
            while True:
                try:
                    url, keys, deep, content = self.spiderManager.parse_queue.get(block=True, timeout=5)
                    executor.submit(self.worker.html_parse, url, keys, deep, content) \
                        .add_done_callback(partial(self.callback, url, keys, deep))
                except queue.Empty:
                    if self.spiderManager.Parse_Sta == ThreadSta.Finish:
                        break

    def callback(self, url, keys, deep, value):
        self.spiderManager.parse_queue.task_done()
        parse_result, url_list, save_list = value.result()

        if parse_result > 0:
            for _url, _keys in url_list:
                self.spiderManager.fetch_queue.put_nowait([_url, _keys, deep+1])
            for item in save_list:
                self.spiderManager.save_queue.put_nowait([url, keys, item])
        else:
            self.spiderManager.save_queue.put_nowait([url, keys, False])


if __name__ == '__main__':
    qa = TaskQueue(queue.Queue())
    qb = TaskQueue(queue.Queue())
    qc = TaskQueue(queue.Queue())

    worker = ParseWorker()
    for i in range(100):
        qb.put_nowait([1, 2, 3, "task %s" % i])

    parse = ParseThread(worker, 3, qa, qb, qc)
    parse.start()
    parse.join()
    pass
