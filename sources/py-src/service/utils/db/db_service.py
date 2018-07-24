from service.utils.db.db_core import Conn
from service.utils import conf


class ConnContext():
    """上下文操作数据库"""

    def __init__(self):
        self.db = Conn()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_t, exc_v, traceback):
        if hasattr(self.db.conn, "commit"):
            self.db.conn.commit()
        print("----关闭数据库---")
        self.db.close()


def db_conn(func):
    def inner(*args, **kwargs):
        result = None
        db = Conn()
        result = func(db, *args, **kwargs)
        if hasattr(db.conn, "commit"):
            db.conn.commit()
        db.close()
        print("-----关闭数据库-----")
        return result

    return inner


@db_conn
def db_insert(db, tb, keys, values):
    return db.insert(tb, keys, values)


@db_conn
def db_get(db, sql):
    return db.get(sql)

@db_conn
def db_get_where_dict(db, tb, where_dict):
    return db.get_where_dict(tb, where_dict)

@db_conn
def db_find(db, sql):
    return db.find(sql)

@db_conn
def db_find_where_dict(db, tb, where_dict):
    return db.find_where_dict(tb, where_dict)

@db_conn
def db_update(db, tb, sets_str, where):
    return db.update(tb, sets_str, where)


@db_conn
def db_insert_dict(db, tb, dict_data):
    return db.insert_dict(tb, dict_data)


@db_conn
def db_update_dict(db, tb, dict_data, where='1=1'):
    return db.update_dict(tb, dict_data, where)


@db_conn
def db_has(db, tb, where='1=1'):
    return db.has(tb, where='1=1')


@db_conn
def db_remove(db, tb, where):
    return db.remove(tb, where)
