#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : AL

import logging


def allot_logger_just_show(name, level=None, fmt=None):
    '''
    初始化一个logger
    :param name: logger名称
    :param fmt: 日志格式
    :param level: 日志的严重程度
    :return:
    '''
    if level == None:
        level = logging.DEBUG
    if fmt == None:
        fmt = '%(asctime)s : %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)

        con_handler = logging.StreamHandler()
        con_handler.setLevel(logging.DEBUG)
        con_handler.setFormatter(logging.Formatter(fmt, datefmt))

        logger.handlers = [con_handler]


def allot_logger(name, filename, level=None, fmt=None):
    '''
    初始化一个logger
    :param name: logger名称
    :param filename: 日志文件路径
    :param fmt: 日志格式
    :param level: 日志的严重程度
    :return:
    '''
    if level == None:
        level = logging.DEBUG
    if fmt == None:
        fmt = '%(asctime)s - %(module)s.%(funcName)s - %(levelname)s [line:%(lineno)d]: %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)

        con_handler = logging.StreamHandler()
        con_handler.setLevel(logging.DEBUG)
        con_handler.setFormatter(logging.Formatter(fmt, datefmt))

        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(fmt, datefmt))

        logger.handlers = [con_handler, file_handler]


allot_logger('Pspider', '..\Report\Report.log', level=logging.ERROR)
allot_logger_just_show("monitor", level=logging.DEBUG)


def get_logger():
    return logging.getLogger('Pspider')


def get_monitor_logger():
    return logging.getLogger('monitor')

report_logger = get_logger()
montion_logger = get_monitor_logger()

if __name__ == '__main__':
    report_logger.info("test_info")
    report_logger.error("test_error")
    montion_logger.info("test_info")
    montion_logger.error("test_error")
    pass
