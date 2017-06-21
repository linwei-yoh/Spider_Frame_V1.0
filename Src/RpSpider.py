#!/usr/bin/env python4
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import requests
import requests.adapters
import time
import configparser

from Rp_login import account_login
from Mongo_Helper import MongoHelper
from Redis_Helper import RedisClient

from component.Spider import Spider as WebSpider
from component.Schedule import Schedule
from overwrite.Fetch_Worker import RpFetchWorker
from overwrite.Parse_Worker import RpPaeseWorker
from overwrite.Save_Worker import RpSaveWorker


# 当前任务中 一个pid对应3个url  key：pid url1:sta url2:sta url3:sta
# 获取一项stax == 0的PID,任意stax == 0,，塞入urlx到爬取队列

# url 状态:0 未处理的url 1 爬取成功的URL 2 爬取失败的URL
# 爬取URL时候遇到 ConnectionError   url状态设置为0 即不进行修改
# 爬取失败/解析失败                 url状态设置为2
# 在save解析内容后                  url状态设置为1

# 遇到网络问题/账号抢登，等使后续爬取无效的情况，需要终止所有的爬取线程，
# 并等待现有的解析 和 存储线程完成 并退出


def RpSpider_Start():
    # 持久化数据库
    mongo_client = MongoHelper()
    # 缓存数据库
    redis_client = RedisClient()

    task_list = mongo_client.get_valid_task()
    task_size = len(task_list)
    print("待处理task数量 : %s" % task_size)
    if task_size == 0:
        print("无需要处理的task")
        return

    config = configparser.ConfigParser()
    config.read("config.ini")

    user_name = config.get("rp_account", "username")
    pass_word = config.get("rp_account", "password")
    max_retries = int(config.get("spider", "retry_times"))
    thread_num = int(config.get("spider", "thread_num"))
    parser_num = int(config.get("spider", "parser_num"))
    monitor_time = int(config.get("spider", "monitor_time"))
    start_time = config.get("spider", "fast_start")
    end_time = config.get("spider", "fast_end")
    fast_fcy = int(config.get("spider", "fast_fcy"))
    nor_fcy = int(config.get("spider", "nor_fcy"))
    fetch_interval = int(config.get("spider", "fetch_interval"))

    schedule = Schedule(start_time, end_time, fast_fcy, nor_fcy, fetch_interval)

    while True:
        print("爬取开始:-----------------")
        with requests.Session() as session:

            session.mount('https://', requests.adapters.HTTPAdapter(pool_maxsize=thread_num))
            session.mount('http://', requests.adapters.HTTPAdapter(pool_maxsize=thread_num))

            # login
            result = account_login(session, user_name, pass_word)
            if result is False:
                print("延时5s后重新登录")
                time.sleep(5)
                continue

            # 配置组件
            fetch_worker = RpFetchWorker(session, max_repeat=max_retries)
            parse_worker = RpPaeseWorker()
            save_worker = RpSaveWorker(mongo_client)
            rp_spider = WebSpider(fetch_worker, parse_worker, save_worker, schedule, redis_client)

            # 根据任务状态表 添加任务队列
            print("开始载入task:-----------------")
            for task in task_list:
                pid, suburb, task_detail, task_otm, task_ad = task
                url = str(pid)
                if task_ad == 0:
                    rp_spider.set_start_url(url, ["ad", suburb])
                if task_otm == 0:
                    rp_spider.set_start_url(url, ["otm", suburb])
                if task_detail == 0:
                    rp_spider.set_start_url(url, ["detail", suburb])

            print("载入task完成:-----------------")
            # fetcher_num 采集线程数
            rp_spider.start_work_and_wait_done(fetcher_num=thread_num, parser_num=parser_num, monitor_time=monitor_time)

        task_list = mongo_client.get_valid_task()
        task_size = len(task_list)
        if task_size > 0:
            print("剩余待处理task数量 : %s" % task_size)
            print("延时10s 再次开始")
            time.sleep(10)
        else:
            print("爬取完成  收工")
            break


if __name__ == '__main__':
    RpSpider_Start()
