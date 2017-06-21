#!/usr/bin/env python4
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import queue
import time
from threading import Thread
from logger_config import montion_logger,report_logger
from component.Task_Queue import TaskQueue
from Spider_Manager import ThreadSta


class MonitorThread(Thread):
    def __init__(self, spiderManager, sleeptime=5):
        Thread.__init__(self, name='Monitor', daemon=True)
        self._sleeptime = sleeptime
        self._IdleTime = ((60 * 5) // sleeptime) if sleeptime < 60 * 5 else 1  # 5m
        self.spiderManager = spiderManager

        self._init_time = 0  # initial time of this spider
        self._last_fetch_num = 0  # fetch number in last time
        self._last_parse_num = 0  # parse number in last time
        self._last_save_num = 0  # save number in last time

        self.ErrorCount = 0

    def run(self):
        self.spiderManager.Monitor_Sta = ThreadSta.Work
        try:
            self._run()
        except Exception:
            self.spiderManager.Monitor_Sta = ThreadSta.Error
            report_logger.error("MonitorThread 出错")

    def _run(self):
        while True:
            time.sleep(self._sleeptime)
            self._init_time += self._sleeptime
            m, s = divmod(self._init_time, 60)
            h, m = divmod(m, 60)

            fetch_rec, fetch_fin = self.spiderManager.fetch_queue.get_count()
            parse_rec, parse_fin = self.spiderManager.parse_queue.get_count()
            save_rec, save_fin = self.spiderManager.save_queue.get_count()
            dif_fetch = fetch_fin - self._last_fetch_num
            dif_parse = parse_fin - self._last_parse_num
            dif_save = save_fin - self._last_save_num

            info = "fetch=(%d/%d,%d) " % (fetch_fin, fetch_rec, dif_fetch)
            info += "parse=(%d/%d,%d) " % (parse_fin, parse_rec, dif_parse)
            info += "save=(%d/%d,%d) " % (save_fin, save_rec, dif_save)
            info += "times=%02d:%02d:%02d" % (h, m, s)

            self._last_fetch_num = fetch_fin
            self._last_parse_num = parse_fin
            self._last_save_num = save_fin

            montion_logger.debug(info)

            if dif_fetch == 0 and dif_parse == 0 and dif_save == 0:
                self.ErrorCount += 1
                if self.ErrorCount >= self._IdleTime:
                    self.ErrorCount = 0
                    self.spiderManager.Monitor_Sta = ThreadSta.Error
                    report_logger.error("MonitorThread 长时间无进展")
                    break
            else:
                self.ErrorCount = 0

            if self.spiderManager.Monitor_Sta == ThreadSta.Finish:
                break


if __name__ == '__main__':
    a = TaskQueue(queue.Queue())
    b = TaskQueue(queue.Queue())
    c = TaskQueue(queue.Queue())
    motior = MonitorThread(a, b, c, 5)
    motior.start()
    motior.join()
    pass
