import json

from service.utils import tool,conf
from service.utils.db.db_service import db_get_where_dict, db_find_where_dict


def data_service_get(tb,dict,key):
    records = db_find_where_dict(tb,dict)
    values = tool.decrypt_db_val(key,records,conf.pro_no_secrets)
    if len(values)>0:
        return values[0]
    else:
        return False
