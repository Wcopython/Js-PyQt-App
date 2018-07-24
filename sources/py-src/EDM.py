#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import PyQt5
from PyQt5.QtWidgets import QApplication

from client.client import QUnFrameWindow
from service.controller.controller import Controller
from service.to_data.dataHandler import DataHandler
from service.to_file.fileHandler import FileHandler
from service.to_word.wordHandler import docHandler
from service.utils import context, conf,tool



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # 开启窗口
    win = QUnFrameWindow()

    # 窗口实例放入上下文中
    context.win = win

    win.loadPage(tool.readHtml(conf.login_page_path()))
    win.show()


    '''
    开启debug模式
    '''
    # win.startDebugger()
    # win.debugger.show()

    sys.exit(app.exec_())
