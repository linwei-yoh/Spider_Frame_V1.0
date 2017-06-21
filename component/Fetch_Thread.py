#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import queue

from Spider_Manager import ThreadSta
from logger_config import report_logger
from functools import partial


class FetchWorker(object):
    """
    覆盖url_fetch方法
    """

    def __init__(self, max_repeat):
        self.max_repeat = max_repeat

    def url_fetch(self, url, keys, deep, repeat):
        result = url + " done"
        return result


class FetchThread(Thread):
    def __init__(self, worker, num, spiderManager):
        """
        建立爬取线程
        :param worker: 爬取处理类
        :param num: 爬取线程最大数量
        :param spiderManager: 爬虫管理

        """
        Thread.__init__(self, name='Fetcher')
        self.worker = worker
        self.num = num
        self.spiderManager = spiderManager

    def run(self):
        self.spiderManager.Fetch_Sta = ThreadSta.Work
        try:
            self._run()
        except Exception as exc:
            report_logger.error("FetchThread ", exc)
            self.spiderManager.Fetch_Sta = ThreadSta.Error

    def _run(self):
        with ThreadPoolExecutor(max_workers=self.num) as executor:
            while True:
                try:
                    url, keys, deep, repeat = self.spiderManager.fetch_queue.get(block=True, timeout=5)
                    executor.submit(self.worker.url_fetch, url, keys, repeat) \
                        .add_done_callback(partial(self.callback, url, keys, deep, repeat))
                except queue.Empty:
                    if self.spiderManager.Fetch_Sta == ThreadSta.Finish:
                        break

    def callback(self, url, keys, deep, repeat, value):
        self.spiderManager.fetch_queue.task_done()  # 可能因为线程池报错而没执行到

        fetch_result, content = value.result()
        # 爬取成功
        if fetch_result > 0:
            self.spiderManager.parse_queue.put_nowait([url, keys, deep, content])
        # 重新爬取
        elif fetch_result == 0:
            self.spiderManager.fetch_queue.put_nowait([url, keys, deep, repeat + 1])
        # 爬取失败
        elif fetch_result == -1:
            self.spiderManager.save_queue.put_nowait([url, keys, False])
        # 致命性失败
        elif fetch_result == -2:
            self.spiderManager.fetch_queue.is_valid = False


if __name__ == '__main__':
    # qa = queue.Queue()
    # qb = queue.Queue()
    # qc = queue.Queue()
    # worker = FetchWorker(max_repeat=3)
    # for i in range(10):
    #     qa.put_nowait("task %s" % i)
    #
    # fetch_t = FetchThread(worker, 3, qa, qb, qc)
    # fetch_t.start()
    # fetch_t.join()
    pass
