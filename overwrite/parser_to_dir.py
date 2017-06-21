#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : AL

from bs4 import BeautifulSoup
import re
from dateutil.parser import parse
import pandas as pd

patten_str = r"/asset/(.*?)/resize"


def parse_detail(content):
    soup = BeautifulSoup(content, "lxml")
    base_dir = dict()
    save_list = [base_dir]

    return [], save_list


def parse_json_otm(content):
    sale_h_dir = dict()
    sale_list = [sale_h_dir]
    return 1, sale_list


def parse_json_ad(content):
    ad_dir = dict()
    return 1, [ad_dir]


if __name__ == '__main__':
    pass
