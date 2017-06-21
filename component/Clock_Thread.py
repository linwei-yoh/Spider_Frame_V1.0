#!/usr/bin/env python4
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import threading
import time
from datetime import datetime, timedelta

from dateutil.parser import parse
from tzlocal import get_localzone

from component.Schedule import Schedule

from logger_config import report_logger
from Spider_Manager import ThreadSta

# 低内聚
class ClockThread(threading.Thread):
    """
    定时处理线程，用来处理在特定时间段修改爬取任务调度接口中的任务频率
    在start-end 之间的时间段采用fast_fqy ，其他采用slow_fqy
    周6 7维持高速
    """

    def __init__(self, schedule: Schedule,spiderManager):
        threading.Thread.__init__(self, name="clock", daemon=True)
        self.schedule = schedule
        self.spiderManager = spiderManager

    def run(self):
        try:
            self.spiderManager.Clock_Sta = ThreadSta.Work
            self.check_date()
        except Exception:
            report_logger.error("Clock_Thread 线程出错")
            self.spiderManager.Clock_Sta = ThreadSta.Error

    def check_date(self):
        while True:
            local_zone = get_localzone()
            start_date = local_zone.localize(parse(self.schedule.start))
            end_date = local_zone.localize(parse(self.schedule.end))
            curr_date = local_zone.localize(datetime.now())

            if curr_date.isoweekday() in [6, 7]:
                self.schedule.fcy_turn_fast()
                tar_date = curr_date + timedelta(days=(8 - curr_date.isoweekday()))
                tar_date = datetime(tar_date.year, tar_date.month, tar_date.day)
                tar_date = local_zone.localize(tar_date)
                time.sleep((tar_date - curr_date).total_seconds())
            else:
                if self.schedule.over_night:
                    if curr_date > start_date:
                        self.schedule.fcy_turn_fast()
                        tar_date = end_date + timedelta(days=1)
                        time.sleep((tar_date - curr_date).total_seconds())
                    elif curr_date < end_date:
                        self.schedule.fcy_turn_fast()
                        time.sleep((end_date - curr_date).total_seconds())
                    else:
                        self.schedule.fcy_turn_slow()
                        time.sleep((start_date - curr_date).total_seconds())
                else:
                    if start_date < curr_date < end_date:
                        self.schedule.fcy_turn_fast()
                        time.sleep((end_date - curr_date).total_seconds())
                    else:
                        self.schedule.fcy_turn_slow()
                        if start_date >= end_date:
                            time.sleep(24 * 60 * 60 - (start_date - start_date).total_seconds())
                        else:
                            time.sleep((start_date - curr_date).total_seconds())


if __name__ == '__main__':
    schedule = Schedule("23:00", "6:00", 100, 10)
    clock = ClockThread(schedule)
    clock.start()
    clock.join()
