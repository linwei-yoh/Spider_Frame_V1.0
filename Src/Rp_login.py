#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : AL

from utilities import make_random_useragent


Login_Url = 'https://login.html'
Login_Header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Length': '47',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': '',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
                }


def account_login(session, username, password):
    Login_Header["User-Agent"] = make_random_useragent()
    data = {'j_username': username, 'j_password': password}
    print("开始登录:-----------------")

    try:
        s = session.post(Login_Url, data=data, headers=Login_Header, timeout=(9.1, 30))
    except Exception:
        print('登录失败')
        return False

    if s.url == 'https://200':
        print(username + ' 登陆成功')
        return True
    else:
        print(username + ' 登录失败')
        return False


if __name__ == '__main__':
    pass
