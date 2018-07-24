import json

from PyQt5.QtCore import QObject, pyqtSlot
from service.to_data.dataService import data_service_get
from service.utils import conf, context, tool



class Controller(QObject):

    @staticmethod
    def render_apply_page(apply):
        context.win.loadPage(tool.readHtml(conf.main_page_path()))
        apply["upfilesPath"] = conf.upfile_path()
        apply["mode"] = "apply"
        apply["applyTitle"] = apply["company_name"]+apply["evalname"]+"申请书"
        context.win.runJS("__allLoaded__ && __allLoaded__('%s')"%(json.dumps(apply)))
        context.win.changeinfo(apply['proxy'], '代理人', 'red', apply["company_name"])

    @pyqtSlot(str, str, result=str)
    def login(self, account, pwd):
        # 01成功 02错误  03异常
        result = "03"
        try:
            print(account, pwd)

            apply = data_service_get("apply", {"account": account}, pwd)

            if apply and apply["password"] == pwd:
                self.render_apply_page(apply)
            else:
                result = "02"

        except Exception as e:
            print(e)
            result = "03"
        return result
