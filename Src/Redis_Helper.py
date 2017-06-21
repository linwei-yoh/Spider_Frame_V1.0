#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import redis
import json
import configparser

IDLE_TASKS = "idle_tasks"  # flag of idle_tasks


class RedisClient(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config.get("redis", "host")
        port = int(config.get("redis", "port"))
        pool = redis.ConnectionPool(host=host, port=port)
        self.client = redis.StrictRedis(connection_pool=pool)
        self.flush_all()

    def flush_all(self):
        """初始化所有用到的key"""
        self.client.flushall()

    def add_idle_task(self, url: str, key: str):
        """插入一个任务到redis爬取任务列表并返回当前列表长度"""
        return self.client.lpush(IDLE_TASKS, json.dumps([url, key]))

    def get_idle_task(self, num=1):
        """
        获得指定数量的空闲任务，没有空闲任务则返回[],数量不足则返回已有的
        每获取一个空闲任务，则爬取任务接收数量+1
        :param num: 需求的任务数量
        :return: [[pid,keys],]
        """
        if self.client.llen(IDLE_TASKS) == 0:
            return []

        result = list()
        for i in range(num):
            item = self.client.lpop(IDLE_TASKS)
            if item is None:
                break
            result.append(json.loads(item.decode()))
        return result

    def get_idle_tasks_size(self):
        """获取空闲任务数量"""
        return self.client.llen(IDLE_TASKS)


if __name__ == '__main__':
    redis_client = RedisClient()
    redis_client.add_idle_task(str(123456),"detail")
    result = redis_client.get_idle_task(10)
    print('tasks', result)

    redis_client.flush_all()
