#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'


from component.Save_Thread import SaveWorker


class RpSaveWorker(SaveWorker):
    def __init__(self, client):
        SaveWorker.__init__(self)
        self.client = client

    def result_save(self, url, keys, item):
        task_name = {"detail": "task_detail", "otm": "task_otm", "ad": "task_ad"}

        task_type = keys[0]
        if task_type in ['detail', 'otm', 'ad']:
            if item is False:
                self.client.update_task_record(url, task_name[task_type], 2)
            else:
                item["Suburb"] = keys[1]
                if self.client.insert_detail_page(url, item):
                    self.client.update_task_record(url, task_name[task_type], 1)


if __name__ == '__main__':
    pass
