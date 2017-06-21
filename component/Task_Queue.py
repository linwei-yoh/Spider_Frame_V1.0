#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import queue
from queue import Queue


class TaskQueue(object):
    """
    一个对队列对象再封装的类，提供任务接收和完成记录，以及队列有效状态
    """
    def __init__(self, q: Queue):
        self._channel = q
        self._receive = 0
        self._finish = 0
        self._valid = True

    @property
    def is_valid(self):
        return self._valid

    @is_valid.setter
    def is_valid(self, value):
        if isinstance(value, bool):
            self._valid = value
        else:
            raise TypeError

    def get_count(self):
        return self._receive, self._finish

    def is_counter_equal(self):
        return True if self._receive == self._finish else False

    def put_nowait(self, item):
        if self._valid:
            self._channel.put_nowait(item)
            self._receive += 1
            return True
        else:
            return False

    def get(self, block=True, timeout=None):
        if not self._valid:
            raise queue.Empty
        task = self._channel.get(block, timeout)
        return task

    def task_done(self):
        self._finish += 1
        self._channel.task_done()

    def qsize(self):
        return self._channel.qsize()


if __name__ == '__main__':
    Q = TaskQueue(queue.Queue())
    for i in range(20):
        Q.put_nowait(i)
    print(Q.qsize())

    while True:
        try:
            item = Q.get(block=True, timeout=1)
            Q.task_done()
        except Exception:
            break
        else:
            print(item)
            print(Q.get_count())

    print(Q.is_valid)
    Q.is_valid = False
    print(Q.is_valid)