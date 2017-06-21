#!/usr/bin/env python4
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from pymongo import MongoClient
import pymongo.errors
import pymongo
import configparser

from component.logger_config import report_logger as logger

data_base = 'rp_data'
page_table = 'rp_detail'
task_table = 'task_record'


# 前置1:安装mongodb完成，且手动建立一个文件作为mongodb的db存放路径
# 前置2:运行前必须先开启mongodb的服务

# 如何开启mongodb
# 方法1.将mongodb 加入windows服务 具体需要查询
# 方法2.在cmd 进入mongodb的安装目录 server/../bin路径
#       执行 mongod.exe --dbpath <db的存放路径> 例如MongoDB/data/db
# server/../bin路径下的mongo.exe简易的客户端交互shell在服务启动后可直接运行
# mongo 的 $currentDate 获得的是utc时间 目前获得的数据类型是datetime.datetime


class MongoHelper(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config.get("mongo", "host")
        port = config.get("mongo", "port")
        self.client = MongoClient(host, int(port))
        self.database = self.client[data_base]
        self.detail_table = self.database[page_table]
        self.task_table = self.database[task_table]

    def recreate(self):
        """
        慎用！ 删除一个数据库的内容，重新建立表和索引  慎用！
        :return: T/F
        """
        self.client.drop_database(data_base)
        return self.create_index()

    def create_index(self):
        """
        建立唯一索引索引 
        :return: T/F
        """
        # 对一个表建立 复合 唯一索引，且在后台执行
        # dropDups在3.0和之后的mongodb中不再被支持，遇到重复文档则会报错
        self.database = self.client[data_base]
        self.detail_table = self.database[page_table]
        self.task_table = self.database[task_table]
        try:
            self.detail_table.create_index([("PropertyID", pymongo.ASCENDING)], unique=True, background=True)
            self.task_table.create_index([("PropertyID", pymongo.ASCENDING)], unique=True, background=True)
        except pymongo.errors.DuplicateKeyError:
            print("创建索引失败，已存在重复数据")
            logger.error("创建索引失败")
            return False
        return True

    def insert_task(self, pid_items: list):
        """
        插入任务队列
        :param pid_items: [(pid,suburb),]
        :return: 
        """
        try:
            tasks = [{"PropertyID": str(pid), "Suburb": suburb, "task_detail": 0, "task_otm": 0, "task_ad": 0} for
                     pid, suburb in pid_items]
            self.task_table.insert_many(tasks, ordered=False)

        except IndexError as e:
            logger.error("pid param error :" + str(e))
        except Exception as e:
            logger.warning(e)

    def reset_task_record(self):
        try:
            self.task_table.update_many({}, {"$set": {"task_detail": 0, "task_otm": 0, "task_ad": 0}})
            return True
        except Exception:
            logger.error("重置task状态失败")
            return False

    def update_task_record(self, pid, task_name: str, task_sta: int):
        """
        更新task记录状态
        :param pid: int/str pid值
        :param task_name: 任务名
        :param task_sta: 任务更新状态
        :return: 
        """
        try:
            self.task_table.update_one({"PropertyID": str(pid)}, {"$set": {task_name: task_sta}})
        except Exception as e:
            logger.error("更新任务记录失败 id : %s\n%s" % (pid, e))

    def get_valid_task(self):
        """
        获得还有未完成任务的URL，每个URL对应三个人物的完成情况
        :return: 各自包含三个任务完成情况的url任务记录列表  [(1,2,0),(1,1,1),(0,0,0),...]
        """
        cursor = self.task_table.find({"$or": [{"task_detail": 0}, {"task_otm": 0}, {"task_ad": 0}]},
                        {"_id": 0, "PropertyID": 1, "Suburb": 1, "task_detail": 1, "task_otm": 1, "task_ad": 1})

        task_list = [(task["PropertyID"], task["Suburb"],task["task_detail"],task["task_otm"],task["task_ad"])
                     for task in cursor if task["PropertyID"] is not None]

        return task_list

    def delete_task_record(self):
        """
        清空任务记录表中的内容
        :return: 
        """
        self.task_table.delete_many({})

    def insert_detail_page(self, pid, content: dict):
        """
        插入/更新详细页面数据 输入对应pid的文档不存在则创建,创建时建立createAt字段
        :param pid: int/str pid值
        :param content: {'a':1}
        :return: 
        """
        try:
            self.detail_table.update_one({"PropertyID": str(pid)},
                                         {"$set": content, "$currentDate": {"LastModify": True}}, upsert=True)
            return True
        except Exception:
            logger.error("插入详细页面失败 id : %s" % pid)
            return False

    def find_page_with_pid(self, pid):
        """
        同过pid找到对应的数据，一个pid可能对应多项数据，因为文档更新
        :param pid: int/str
        :return: 返回一个字典列表
        """
        try:
            cursor = self.detail_table.find({"PropertyID": str(pid)}, {"_id": 0})
            results = [doc for doc in cursor]
            return results
        except Exception:
            logger.error("获取页面数据失败 id : %s" % pid)
            return []

    # 当skip和limit组合使用时，无论顺序先skip，再limit
    # 当sort skip limit组合使用时 先sort 再skop 再limit
    # 使用aggregate 能按位置顺序执行skip limit srt
    def find_page_all(self, skip=0, limit=0):
        """
        获取所有页面内容,默认采用pid的升序排序
        :param skip: 跳过前a条记录 0 不跳过 不能为负数
        :param limit: 执行跳过后，最多返回b条记录 0 不限制 不能为负数
        :return: 不包含_id的字典列表 [{},{}]
        """
        try:
            cursor = self.detail_table.find({}, {"_id": 0}) \
                .sort([("PropertyID", pymongo.ASCENDING)]).skip(skip).limit(limit)
            results = [doc for doc in cursor]
            return results
        except Exception:
            logger.error("查询全部页面数据失败 skip:%s limit:%s" % (skip, limit))
            return []


if __name__ == '__main__':
    # 慎用
    MongoDB = MongoHelper()

    if MongoDB.recreate():
        print("数据库完全重置完成")
