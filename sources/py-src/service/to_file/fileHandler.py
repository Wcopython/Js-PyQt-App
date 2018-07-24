import json
import os
import shutil

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog

from service.to_file.fileService import to_zc_zip, unzip_zc_zip
from service.utils import conf


class FileHandler(QObject):
    #选择文件
    @pyqtSlot(result=str)
    def select(self):
        files,type= QFileDialog.getOpenFileNames(None, "选择附件", conf.selectfile_path,conf.selectfile_type)
        print(files)
        return json.dumps(files)

    # 打开本地文件
    @pyqtSlot(str,result=bool)
    def open(self,path):
        try:
            path = os.path.join(conf.app_path,path)
            print("打开本地文件："+path)
            os.startfile(path)
            return True
        except:
            try:
                print("打开本地文件：" + path)
                os.startfile(path)
                return True
            except:
                return False

    #复制文件
    @pyqtSlot(str, str)
    def copy(self,input,target):
        if(os.path.exists(input)):
            print("目标文件：%s"%target)
            dir = os.path.dirname(target)
            if not os.path.exists(dir):
                os.makedirs(dir)
            print("复制文件：input:[{}],output:[{}]".format(input,target))
            shutil.copyfile(input, target)

    #物理删除已删除的文件
    @pyqtSlot(str,result=bool)
    def delFile(self, filePath):
        try:
            if (os.path.exists(filePath)):
                print("物理删除文件："+filePath)
                os.remove(filePath)
            return True
        except:
            return False

    #压缩文件包
    @pyqtSlot(str,str,result=str)
    def zip(self,proId,proKey):
        result = "failed"
        zipName,zipType = QFileDialog.getSaveFileName(None,"导出数据包",conf.zip_target(),conf.zip_type)
        print("导出数据包到："+zipName)
        if(zipName == ""):
            result = "cancel"
        else:
            try:
                result = to_zc_zip(proId,proKey,zipName)
            except Exception as e:
                print(str(e))
        return result

    # 载入压缩文件包
    @pyqtSlot(str,str,result=str)
    def loadZip(self,proId,proKey):
        result = "failed"
        zipName, zipType = QFileDialog.getOpenFileName(None, "导入数据包", conf.get_desktop(), conf.zip_type)
        if (zipName == ""):
            result = "cancel"
        else:
            try:
                result = unzip_zc_zip(zipName,proId,proKey)
            except Exception as e:
                result = "failed"
        return result








