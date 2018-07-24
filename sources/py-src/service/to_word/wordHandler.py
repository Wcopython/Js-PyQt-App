import os

from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtWidgets import QFileDialog

from service.to_word.html_utils import HtmlUtils
from service.utils import conf,context


class docHandler(QObject):
    # 导出word文件
    @pyqtSlot(str,result=str)
    def export_word(self, html_code):
        try:
            docName, docType = QFileDialog.getSaveFileName(None, "导出word", conf.doc_path, conf.doc_type)
            print("导出word地址："+docName)
            if(docName != ''):
                if(os.path.exists(docName)):
                    os.remove(docName)
                conf.doc_path = docName;
                hu = HtmlUtils()
                hu.html_to_word(html_code)
                return 'ok'
        except Exception as e:
            print(str(e))
            return str(e)
