#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from component.Parse_Thread import ParseWorker
from component.logger_config import report_logger
from parser_to_dir import parse_detail, parse_json_ad, parse_json_otm


class RpPaeseWorker(ParseWorker):
    def html_parse(self, url, keys, deep, content):
        try:
            parse_result, url_list, save_list = self.working(keys[0], content)
        except Exception as excep:
            parse_result, url_list, save_list = -1, [], []
            report_logger.error("keys=%s, deep=%s, url=%s,msg=%s" % (keys, deep, url, excep))

        if 0 <= self.max_deep <= deep:
            url_list = []
        return parse_result, url_list, save_list

    def working(self, keys, content):
        if keys == "detail":
            url_list, save_list = parse_detail(content)
            return 1, url_list, save_list
        elif keys == "otm":
            result, save_list = parse_json_otm(content)
            return result, [], save_list
        elif keys == 'ad':
            result, save_list = parse_json_ad(content)
            return result, [], save_list
        else:
            return -1, [], []


if __name__ == '__main__':
    pass
