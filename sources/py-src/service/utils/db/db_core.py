# python sqlite
import os
import sqlite3
import uuid

from PyQt5.QtWidgets import QMessageBox

from service.utils import conf


class Conn():
    def __init__(self):
        path = conf.db_path()
        # QMessageBox.information(None,"标题",path,QMessageBox.Yes | QMessageBox.No)
        print("数据库地址：" + path)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        if os.path.exists(path) and os.path.isfile(path):
            self.cursor = self.conn.cursor()
        else:
            self.cursor = None

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.conn.close()

    def insert(self, tb, keys, values):
        '''插入数据'''
        result = False
        try:
            if tb != '' and len(keys) > 0 and len(values) > 0:
                if len(keys) == len(values):
                    values = ['\"{}\"'.format(item) if isinstance(item, str) else str(item) for item in values]
                    sql = 'insert into {}({}) values ({})'.format(tb, ",".join(keys), ",".join(values))
                    print('执行sql:{}'.format(sql))
                    self.cursor.execute(sql)
                    result = True
        except Exception as e:
            print(str(e))

        return result

    def get(self, sql):
        '''查询一条数据'''
        result = False
        try:
            result_list = self.find(sql)
            if len(result_list) > 0:
                result = result_list[0]
        except Exception as e:
            print(e)
        return result

    def find(self, sql):
        try:
            if sql is not None and sql != '':
                print('执行sql:[{}]'.format(sql))
                self.cursor.execute(sql, '')
                records = self.cursor.fetchall()
                return records
            else:
                return []
        except Exception as e:
            print(e)
            return []

    def update(self, tb, sets_str, where):
        result = False
        try:
            '''更新数据'''
            if tb != '' and sets_str != '' and where != '':
                sql = 'update {} set {} where {}'.format(tb, sets_str, where)
                print('执行sql:{}'.format(sql))
                self.cursor.execute(sql)
                result = True
        except Exception as e:
            print(str(e))
        return result

    def remove(self, tb, where):
        result = False
        try:
            if tb != '' and where != '':
                sql = 'DELETE FROM {} where {}'.format(tb, where)
                print('执行sql:{}'.format(sql))
                self.cursor.execute(sql)
                result = True
        except Exception as e:
            print(str(e))
        return result

    def has(self, tb, where='1=1'):
        sql = 'select * from %s where %s' % (str(tb), str(where))
        list = self.find(sql)
        return len(list) > 0

    def find_where_dict(self, tb, where_dict):
        where_sql = self.__where_dict_to_sql(where_dict)
        return self.find("select * from %s where %s" % (tb, where_sql))

    def get_where_dict(self, tb, where_dict):
        results = self.find_where_dict(tb, where_dict)
        if len(results) > 0:
            return results[0]
        else:
            return False

    def insert_dict(self, tb, dict_data):
        print(dict_data)
        result = False
        if isinstance(dict_data, dict):
            keys = []
            values = []
            for k, v in dict_data.items():
                keys.append(k)
                values.append(v)
            result = self.insert(tb, keys, values)
        return result

    def update_dict(self, tb, dict_data, where='1=1'):
        result = False
        if isinstance(dict_data, dict):
            sets = []
            for k, v in dict_data.items():
                v_str = '\"{}\"'.format(v) if isinstance(v, str) else str(v)
                sets.append('{}={}'.format(k, v_str))
            result = self.update(tb, ",".join(sets), where)
        return result

    def insert_or_update(self, tb, data, where_dict={}):
        result = False
        try:
            where_sql = self.__where_dict_to_sql(where_dict)

            if self.has(tb, where_sql):
                result = self.update_dict(tb, data, where_sql)
            else:
                data["id"] = str(uuid.uuid1())
                data.update(where_dict)
                result = self.insert_dict(tb, data)
        except Exception as e:
            print(e)
        return result

    def __where_dict_to_sql(self, dict):
        sets = []
        for k, v in dict.items():
            v_str = '\"{}\"'.format(v) if isinstance(v, str) else str(v)
            sets.append('{}={}'.format(k, v_str))

        return " and ".join(sets) if len(sets) > 0 else '1=1'

    def remove_dict(self, tb, where_dict):
        where_sql = self.__where_dict_to_sql(where_dict)
        return self.remove(tb, where_sql)
