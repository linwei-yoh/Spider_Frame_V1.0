#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from component.Fetch_Thread import FetchWorker
from component.logger_config import report_logger

import time
import requests
from utilities import make_random_useragent

detail_Header = {'Accept': 'text/html, */*; q=0.01',
                 'Accept-Encoding': 'gzip, deflate, sdch, br',
                 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                 'Connection': 'keep-alive',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
                 'X-Requested-With': 'XMLHttpRequest'}

json_Header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
               'Connection': 'keep-alive',
               'Referer': 'asdf.html',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}

otm_param = {'returnFields': 'otmListingSale',
             '_': 1493444149292}

base_url = "https://abc/detail.html?propertyId=%s"
otm_url = "https://avc/%s.json?"
ad_url = "https://avc/%s/advertisements.json"


class RpFetchWorker(FetchWorker):
    def __init__(self, session, max_repeat):
        FetchWorker.__init__(self, max_repeat)
        self.session = session

    def url_fetch(self, url, keys, repeat):
        try:
            fetch_result, content = self.working(url, keys[0])
        except requests.ConnectionError:
            fetch_result, content = -2, None
        except Exception:
            if repeat >= self.max_repeat:
                fetch_result, content = -1, None
            else:
                fetch_result, content = 0, None

        return fetch_result, content

    def working(self, url, key):
        if key == "detail":
            tar_url = base_url % url
            detail_Header['User-Agent'] = make_random_useragent()
            resp = self.session.get(tar_url, headers=detail_Header, params=None, timeout=(6.05, 60),
                                    allow_redirects=False)
            result = resp.text
        elif key == "otm":
            tar_url = otm_url % url
            json_Header['Referer'] = base_url % url
            json_Header['User-Agent'] = make_random_useragent()
            otm_param['_'] = int(time.time() * 1000)
            resp = self.session.get(tar_url, headers=json_Header, params=otm_param, timeout=(6.05, 20),
                                    allow_redirects=False)
            result = resp.json()
        elif key == 'ad':
            tar_url = ad_url % url
            json_Header['Referer'] = base_url % url
            json_Header['User-Agent'] = make_random_useragent()
            resp = self.session.get(tar_url, headers=json_Header, params=None, timeout=(6.05, 20),
                                    allow_redirects=False)
            result = resp.json()
        else:
            report_logger.error("%s keys error: %s is invalid", self.__class__.__name__, key)
            return -1, None  # 不会执行到的部分

        if resp.status_code == 200:
            return 1, result
        # 需要确认 账号抢登 /网络断开 是否全都能捕获到 503中
        elif resp.status_code == 503:
            raise requests.ConnectionError
        else:
            resp.raise_for_status()


if __name__ == '__main__':
    pass
