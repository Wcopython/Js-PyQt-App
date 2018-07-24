import json
import uuid

from PyQt5.QtCore import QObject, pyqtSlot

from service.utils.db.db_service import db_find, db_insert_dict, db_update_dict, ConnContext
from service.utils import tool, conf


class DataHandler(QObject):
    # 查询记录集,返回数组形式[{id:'',name:''},{id:'',name:''}]
    @pyqtSlot(str, str, result=str)
    def find(self, serialId, sql):
        try:
            records = db_find(sql)
            value = tool.decrypt_db_val(serialId, records, conf.pro_no_secrets)
            value = json.dumps(value)
            print(value)
            return value
        except:
            return ''

    # 新增表记录
    @pyqtSlot(str, str, str, result=bool)
    def insert(self, serialId, tb, data):
        result = True
        try:
            dict = json.loads(data)
            tool.encrypt_db_val(serialId, dict, conf.pro_no_secrets)
            db_insert_dict(tb, dict)
        except:
            result = False
        return result

    # 更新表记录
    @pyqtSlot(str, str, str, str, result=bool)
    def update(self, serialId, tb, data, where):
        result = True
        try:
            dict = json.loads(data)
            tool.encrypt_db_val(serialId, dict, conf.pro_no_secrets)
            db_update_dict(tb, dict, where)
        except:
            result = False
        return result

    @pyqtSlot(str, str, result=bool)
    def batchSave(self, serialId, data):
        result = False
        print(data)
        data = json.loads(data)
        try:
            # 添加或修改申请书数据
            with ConnContext() as conn:
                for tb, fields in data.items():
                    apply_id = fields["apply_id"]
                    tool.encrypt_db_val(serialId, fields, conf.pro_no_secrets)
                    conn.insert_or_update(tb, fields, {"apply_id": apply_id})

                # 修改申请书修改时间
                conn.update_dict("apply", {"update_date": tool.get_now_time()}, "pro_id='%s'" % apply_id)
            result = True
        except Exception as e:
            print(e)
        return result

    @pyqtSlot(str, str, result=str)
    def batchFind(self, serialId, data):
        print(data)
        result = ''
        data = json.loads(data)
        applyId = data["apply_id"]
        try:
            db_data = {}
            with ConnContext() as conn:
                for tb in data["tables"]:
                    records = conn.find_where_dict(tb, {"apply_id": applyId})
                    results = tool.decrypt_db_val(serialId, records, conf.pro_no_secrets)
                    if len(results) > 0:
                        db_data[tb] = results[0]
                        print(tb, results[0])
            result = json.dumps(db_data)
        except Exception as e:
            print(e)
        return result
