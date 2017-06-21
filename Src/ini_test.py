#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import configparser


def read_ini():
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
    print(user_name, pass_word)
    print(max_retries, thread_num, parser_num, monitor_time)
    print(start_time, end_time, fast_fcy, nor_fcy, fetch_interval)


if __name__ == '__main__':
    read_ini()
