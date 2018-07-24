import ctypes
import os
from PyQt5 import QtCore

from PyQt5.QtCore import QRect, QUrl, QSize, QPoint, Qt
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QFont
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSizePolicy, QHBoxLayout, QMessageBox, QDesktopWidget, \
    QPushButton, QLabel, QApplication
from idna import unicode

from service.controller.controller import Controller
from service.to_data.dataHandler import DataHandler
from service.utils import context
# from service.utils.tool import removeDir
from client import resource
from client import web
from service.to_file.fileHandler import FileHandler
from service.to_word.wordHandler import docHandler
from service.utils import conf,tool

global imax
global movenum
global nortomax
imax=0#为0时代表是窗口状态，为1时代表已经是最大化状态
movenum=0 #因为窗口状态时有8像素的阴影，最大化时没有，在动态调整窗口关闭等按钮组的位置时需要考虑这个位置差值参数
allowresize=1#为0时不允许边角拖拽调整大小，为1时允许
numbinfo=1#为0时不显示用户信息区，为1时显示

def web_path():
    # return "file:///C:/Users/Administrator/Desktop/webpackEDM/src/js/components/index.html"
    return "file:///"+conf.app_path+"/lib/page/dist/index.html"

apptitle="测评风评数据管理系统"
# webkiturl='qrc:/index.html'
# webkiturl = web_path()

titleheight=80
infobgimgwidth=230
infotopwidth=25#信息区的顶部留空高度
infoIndent=40#信息区文字缩进
infofont='微软雅黑'
appicon=':/img/EDM.ico'
infobgimg=":/img/infobg.png"
titleimg=":/img/title.png"
windowminW=916#窗体最小宽度
windowminH=600#窗体最小高度
qssfile=":/EDM.qss"


class QTitleLabel(QLabel):

    """
    新建标题栏标签类
    """
    def __init__(self, *args):
        super(QTitleLabel, self).__init__(*args)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

#-----------------------------增加双击top图最大化和恢复的功能
    def mouseDoubleClickEvent(self,w):
        #print('mouse double clicked')
        global imax
        if imax==0:
            QUnFrameWindow._changeNormalButton(context.win)
        elif imax==1:
            QUnFrameWindow._changeMaxButton(context.win)




class QTitleButton(QPushButton):
    """
    新建标题栏按钮类
    """
    def __init__(self, *args):
        super(QTitleButton, self).__init__(*args)
        self.setFont(QFont("Webdings")) # 特殊字体以不借助图片实现最小化最大化和关闭按钮
        self.setFixedWidth(40)



class QUnFrameWindow(QWidget):
    def __init__(self):
        global apptitle
        super(QUnFrameWindow, self).__init__(None,Qt.FramelessWindowHint) # 设置为顶级窗口，无边框
        self._padding =5 # 设置边界宽度为5
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.SHADOW_WIDTH = 8
        self.setWindowTitle(apptitle)
        self.initLayout() # 设置框架布局
        #self.setMinimumSize(900,700)
        self.setMouseTracking(True) # 设置widget鼠标跟踪
        self.initDrag() # 设置鼠标跟踪判断默认值

        # self.setStyleSheet(open(qssfile).read())
        self.file = QtCore.QFile(qssfile)
        self.file.open(QtCore.QFile.ReadOnly)
        self.styleSheet = self.file.readAll()
        self.styleSheet = unicode(self.styleSheet, encoding='utf8')
        self.setStyleSheet(self.styleSheet)


        self.setMinimumSize(windowminW,windowminH)
        self.setContentsMargins(8,8,8,8)
        self.setCloseButton(True)
        self.setMinMaxButtons(True)
        self.center()



    #------------------------------------绘制边框阴影
    def drawShadow(self,painter):
        #print('ddddddddddddddddddd')
        #绘制左上角、左下角、右上角、右下角、上、下、左、右边框
        #print(self._tomax_drag)
        self.pixmaps=[]
        if imax==0:
            if self._tomax_drag==False:
                self.pixmaps= [':/shadow/shadow_left_top.png', ':/shadow/shadow_left_bottom.png', ':/shadow/shadow_right_top.png', ':/shadow/shadow_right_bottom.png',':/shadow/shadow_top.png', ':/shadow/shadow_bottom.png', ':/shadow/shadow_left.png',':/shadow/shadow_right.png']

                # self.pixmaps= ['./shadow/shadow_left_top.png', './shadow/shadow_left_bottom.png', './shadow/shadow_right_top.png', './shadow/shadow_right_bottom.png','./shadow/shadow_top.png', './shadow/shadow_bottom.png', './shadow/shadow_left.png','./shadow/shadow_right.png']
            else:
                self.pixmaps = [':/shadow/shadow_left_top_m.png', ':/shadow/shadow_left_bottom_m.png',':/shadow/shadow_right_top_m.png',':/shadow/shadow_right_bottom_m.png',':/shadow/shadow_top_m.png', ':/shadow/shadow_bottom_m.png',':/shadow/shadow_left_m.png', ':/shadow/shadow_right_m.png']

                # print('yyyy')
                # self.pixmaps = ['./shadow/shadow_left_top_m.png', './shadow/shadow_left_bottom_m.png','./shadow/shadow_right_top_m.png','./shadow/shadow_right_bottom_m.png','./shadow/shadow_top_m.png', './shadow/shadow_bottom_m.png','./shadow/shadow_left_m.png', './shadow/shadow_right_m.png']


            painter.drawPixmap(0, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[0]))   #左上角
            # print(self.pixmaps,self._tomax_drag,'P')
            painter.drawPixmap(self.width()-self.SHADOW_WIDTH, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[2]))   #右上角
            painter.drawPixmap(0,self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[1]))   #左下角
            painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  #右下角
            painter.drawPixmap(0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[6]).scaled(self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH)) #左
            painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[7]).scaled(self.SHADOW_WIDTH, self.height()- 2*self.SHADOW_WIDTH)) #右
            painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[4]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH)) #上
            painter.drawPixmap(self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[5]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH))   #下

    #------------------------------------绘制边框阴影
    def paintEvent(self, event):
        global movenum,infobgimgwidth,infobgimgheight,infobgimg
        # if imax == 0:
        painter = QPainter(self)
        # print('rrrrrrrrrrrrr')
        self.drawShadow(painter)
        # print('444444444')
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRect(QRect(self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.width() - 2 * self.SHADOW_WIDTH,
                              self.height() - 2 * self.SHADOW_WIDTH))
        painter.end()


        if imax==0:
            movenum=8
        elif imax==1:
            movenum=0
        painter1 = QPainter(self)
        # painter1.begin(self)
        painter1.setRenderHint(QPainter.Antialiasing)
        painter1.setPen(Qt.NoPen)
        painter1.drawPixmap(movenum,movenum,infobgimgwidth,titleheight,QPixmap(infobgimg))
        painter1.end()




    # 设置鼠标跟踪判断扳机默认值
    def initDrag(self):
        #为FALSE时代表未有相关动作状态
        self._move_drag = False#针对是否是在最大化状态时拖动状态的标记，为True时代表正在按压拖动中，用来一次性重新定位窗体在恢复窗口后鼠标拖拽的位置（宽度居中，标题图片一般高度，move方法中）
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._maxmove_drag=False
        self._tomax_drag=False

    # def initTitleLabel(self):
    # #     # 安放标题栏标签
    #     self._TileLabel = QTitleLabel(self)
    #     #self._TitleLabel.setMouseTracking(True) # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
    #     self._TitleLabel.setIndent(10) # 设置标题栏文本缩进
    #     #self._TitleLabel.move(0, 0) # 标题栏安放到左上角




    def initLayout(self):
        # 设置框架布局
        global numbinfo,titleheight,infobgimgwidth,infotopwidth,infoIndent,infofont,appicon,titleimg

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowIcon(QIcon(appicon))
        #添加整体窗体大布局框架
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        #在整体框架里添加竖排layout
        self.verticalLayout =QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout,0,0,0,0)

        #在竖排框架里上方生成一个横排放用户信息和标题栏
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setContentsMargins(0,0,0,0)#浏览器右下方留出拖拽空间
        self.horizontalLayout_1.setObjectName("horizontalLayout1")
        self.verticalLayout.addLayout(self.horizontalLayout_1)


        if numbinfo==1:#如果允许显示用户信息区
# ---------用户信息区框架及里面所有内容
            # 在上方横排里添加竖排layout，放用户信息
            self.verticalLayout_1 = QVBoxLayout()
            self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)

            self.verticalLayout_1.setObjectName("verticalLayout_1")
            # 把竖向框架嵌入到顶部横向框架里
            self.horizontalLayout_1.addLayout(self.verticalLayout_1)

            #添加一个固定宽的label，用于把信息区的宽度撑开
            self.wlab = QTitleLabel()
            self.wlab.setScaledContents(False)
            self.wlab.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self.wlab.setStyleSheet("QTitleLabel{font-size:20px;background-color:rgba(255, 255, 255, 0);}")
            self.wlab.setMinimumWidth(infobgimgwidth)
            self.wlab.setMaximumHeight(infotopwidth)
            #在信息区的竖向框架里添加Wlab，用户名密级横排框架，下面就是账号、部门等label
            self.verticalLayout_1.addWidget(self.wlab)#用wlab撑开信息区的宽度

            # 在用户信息区放置一个横排框架，横向放置用户名和密级信息
            self.horizontalLayout_2 = QHBoxLayout()
            self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)  # 浏览器右下方留出拖拽空间
            self.horizontalLayout_2.setObjectName("horizontalLayout2")
            self.verticalLayout_1.addLayout(self.horizontalLayout_2)

            #信息区的横向框架里放置姓名和密级
            self.namelab = QTitleLabel()
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.namelab.sizePolicy().hasHeightForWidth())
            self.namelab.setSizePolicy(sizePolicy)
            self.namelab.setMinimumSize(QSize(0, 0))
            self.namelab.setObjectName("namelab")
            self.namelab.setScaledContents(False)
            self.namelab.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self.namelab.setStyleSheet("QTitleLabel{ font-size:22px;background-color: rgba(255,255,255,0);}")
            self.namelab.setIndent(infoIndent)
            self.namelab.setFont(QFont(infofont))
            self.namelab.setFixedHeight(24)
            # self.namelab.setAlignment(Qt.AlignTop)
            self.namelab.setText('')
            self.horizontalLayout_2.addWidget(self.namelab, 0, Qt.AlignBottom)

            #姓名后面放个空label间隔姓名和密级
            self.konglab1=QTitleLabel()
            self.konglab1.setFixedWidth(5)
            self.konglab1.setObjectName("konglab1")

            self.konglab1.setText("")
            self.konglab1.setStyleSheet("QTitleLabel{font-size:18px;background-color:rgba(255,255,255,0);}")
            self.horizontalLayout_2.addWidget(self.konglab1)

            #后面跟着密级标签
            self.mijilab = QTitleLabel()
            self.mijilab.setScaledContents(False)
            self.mijilab.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.mijilab.sizePolicy().hasHeightForWidth())
            self.mijilab.setSizePolicy(sizePolicy)
            self.mijilab.setObjectName("mijilab")
            self.mijilab.setText('')
            self.mijilab.setAlignment(Qt.AlignTop)
            self.mijilab.setFont(QFont(infofont))
            self.setRoleColor("rgba(255,255,255,0)")
            # self.mijilab.setStyleSheet("QTitleLabel{border-width: 0px 0px 0px 0px;border-radius:3px;border-color:rgba(255,255,255,0); font-size:12px;border-style: solid;background-color:rgba(255,255,255,0);}")
            self.mijilab.setFixedHeight(17)
            self.horizontalLayout_2.addWidget(self.mijilab, 0, Qt.AlignBottom)

            #后面跟着空label，让姓名和密级标签的宽度已最小化方式呈现
            self.konglab2 = QTitleLabel()
            sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.konglab2.sizePolicy().hasHeightForWidth())
            self.konglab2.setSizePolicy(sizePolicy)
            self.konglab2.setMinimumSize(QSize(0, 0))
            self.konglab2.setStyleSheet("QTitleLabel{background-color: rgba(255,255,255,0);}")
            #self.konglab2.setFixedSize(self.wlab.width()-self.namelab.width()-self.konglab1.width()-self.mijilab.width(),10)
            self.konglab2.setText("")

            self.konglab2.setObjectName("konglab2")
            self.horizontalLayout_2.addWidget(self.konglab2)

            #在用户名和密级下添加竖排的账号信息
            self.numblab = QTitleLabel()
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.numblab.sizePolicy().hasHeightForWidth())
            self.numblab.setSizePolicy(sizePolicy)
            self.numblab.setMinimumSize(QSize(0, 0))
            self.numblab.setObjectName("namelab")
            self.numblab.setScaledContents(False)
            self.numblab.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self.numblab.setStyleSheet("QTitleLabel{ font-size:11px;background-color: rgba(255,255,255,0);}")
            self.numblab.setIndent(infoIndent)
            #self.numblab.setAlignment(Qt.AlignBottom)
            self.numblab.setFont(QFont(infofont))
            self.numblab.setText('')
            self.numblab.setFixedSize(infobgimgwidth,19)
            self.verticalLayout_1.addWidget(self.numblab, 0, Qt.AlignBottom)

            #在用户名和密级下添加竖排的部门信息
            self.bumenlab = QTitleLabel()
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.bumenlab.sizePolicy().hasHeightForWidth())
            self.bumenlab.setSizePolicy(sizePolicy)
            self.bumenlab.setMinimumSize(QSize(0, 0))
            self.bumenlab.setObjectName("bumenlab")
            self.bumenlab.setScaledContents(False)
            self.bumenlab.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self.bumenlab.setStyleSheet("QTitleLabel{ font-size:4px;background-color: rgba(255,255,255,0);}")
            self.bumenlab.setIndent(infoIndent)
            #self.bumenlab.setAlignment(Qt.AlignTop)
            self.bumenlab.setFont(QFont(infofont))
            self.bumenlab.setText('')
            self.bumenlab.setFixedWidth(infobgimgwidth)
            self.verticalLayout_1.addWidget(self.bumenlab)


#-----------------------------添加标题栏图片标签
        self.label = QTitleLabel()
        self.label.setScaledContents(False)
        self.label.setPixmap(QPixmap(titleimg))
        # 设置title标签在布局中是自适应宽度的
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        # 设置title标签高度，无间隙
        self.label.setFixedHeight(titleheight)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setMouseTracking(True)
        #接着把title标签嵌入到顶部横向框架里
        self.horizontalLayout_1.addWidget(self.label)


#---------------在上方整体的横排之下再排生成一个横排放浏览器
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,0,0,0)#浏览器右下方留出拖拽空间
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)

        #生成一个浏览器组件，添加到下方的横排layout
        self.webEngineView = QWebView()
        # self.webEngineView.load(QUrl(web_path()))
        self.webEngineView.setObjectName('webEngineView')
        self.webEngineView.setContentsMargins(0,0,0,0)
        self.webEngineView.setMaximumSize(QSize(10000, 10000))
        self.webEngineView.setMouseTracking(True)
        self.horizontalLayout.addWidget(self.webEngineView)



        #  with open("C:/Users/Administrator/Desktop/EDM/填报端/lib/page/dist/main_dist.html", mode='r', encoding='UTF-8') as file_object:
        #
        #     contents = file_object.read()
        #
        #     # print(contents)
        #     self.webEngineView.setHtml(tool.decrypt("123456",contents))
        # # self.webEngineView.load(QUrl(url))


    def closeEvent(self, event):
        try:
            reply = QMessageBox.question(self, '提示',
                                         "确认退出?", QMessageBox.Yes, QMessageBox.No)
            #print(reply == QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                event.accept()
                # self.close()
            else:
                event.ignore()
        except:
            pass

    def setRoleColor(self,color):
        self.mijilab.setStyleSheet("QTitleLabel{border-width: 0px 0px 0px 0px;border-radius:3px;border-color:%s; font-size:12px;border-style: solid;background-color:%s;}"%(str(color),str(color)))


    def changeinfo(self,name="",role="",color="",info=""):
        global numbinfo
        if numbinfo==1:
            self.namelab.setText(name[0:4])
            self.mijilab.setText(' '+ role[0:6] + ' ')
            self.setRoleColor(color)
            self.numblab.setText(info[0:50])





    def setCloseButton(self, bool):
        # 给widget定义一个setCloseButton函数，为True时设置一个关闭按钮
        if bool == True:
            self._CloseButton = QTitleButton(b'\xef\x81\xb2'.decode("utf-8"), self)
            self._CloseButton.setObjectName("CloseButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._CloseButton.setToolTip("关闭窗口")
            self._CloseButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._CloseButton.setFixedHeight(40)

            #self._CloseButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._CloseButton.clicked.connect(self.close) # 按钮信号连接到关闭窗口的槽函数




    def setMinMaxButtons(self, bool):
        # 给widget定义一个setMinMaxButtons函数，为True时设置一组最小化最大化按钮
        if bool == True:
            self._MinimumButton = QTitleButton(b'\xef\x80\xb0'.decode("utf-8"), self)
            self._MinimumButton.setObjectName("MinMaxButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MinimumButton.setToolTip("最小化")
            self._MinimumButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MinimumButton.setFixedHeight(40)  # 设置按钮高度为标题栏高度
            #self._MinimumButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._MinimumButton.clicked.connect(self.showMinimized) # 按钮信号连接到最小化窗口的槽函数
            self._MaximumButton = QTitleButton(b'\xef\x80\xb1'.decode("utf-8"), self)
            self._MaximumButton.setObjectName("MinMaxButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MaximumButton.setToolTip("最大化")
            self._MaximumButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MaximumButton.setFixedHeight(40)
            #self._MaximumButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._MaximumButton.clicked.connect(self._changeNormalButton) # 按钮信号连接切换到恢复窗口大小按钮函数




    def _changeNormalButton(self):
        global imax
        imax=1#已经最大化了
        # 切换到恢复窗口大小按钮
        # self.changeinfo('王骅', '核心商密', '3333333333224561354')
        try:
            self.setContentsMargins(0,0,0,0)

            self.showMaximized() # 先实现窗口最大化
            self._MaximumButton.setText(b'\xef\x80\xb2'.decode("utf-8")) # 更改按钮文本
            self._MaximumButton.setToolTip("恢复") # 更改按钮提示
            self._move_drag = False#针对按住拖到顶端最大化后，就不再相应鼠标拖拽事件
            self._tomax_drag=False
            # self.window().resize(self.width(), self.height() + 1)
            # self.window().resize(self.width(), self.height() - 1)
            self._MaximumButton.disconnect() # 断开原本的信号槽连接

            #self.toplabel.move(0,0)
            #self.toplabel.setFixedWidth(self.width())
            self._MaximumButton.clicked.connect(self._changeMaxButton) # 重新连接信号和槽
        except:
            pass




    def _changeMaxButton(self):
        global imax

        imax = 0
        # 切换到最大化按钮
        try:
            self.setContentsMargins(8, 8, 8, 8)
            self.showNormal()
            self._MaximumButton.setText(b'\xef\x80\xb1'.decode("utf-8"))
            self._MaximumButton.setToolTip("最大化")
            self._tomax_drag = False
            self.window().resize(self.width(), self.height() + 1)
            self.window().resize(self.width(), self.height() - 1)
            self._MaximumButton.disconnect()


            # self.changeinfo('李振飞','机密', '210199292929292212')
            self._MaximumButton.clicked.connect(self._changeNormalButton)
        except:
            pass




    def resizeEvent(self, QResizeEvent):
        global imax
        global movenum

        # 自定义窗口调整大小事件
        if imax==0:
            movenum=8
        elif imax==1:
            movenum=0
            try:
                self.setContentsMargins(0,0,0,0)
            except:
                pass
        # 分别移动三个按钮到正确的位置
        try:
            self._CloseButton.move(self.width() - self._CloseButton.width()-movenum, movenum)
        except:
            pass
        try:
            self._MinimumButton.move(self.width() - (self._CloseButton.width() + 1) * 3 + 1-movenum, 0+movenum)
        except:
            pass
        try:
            self._MaximumButton.move(self.width() - (self._CloseButton.width() + 1) * 2 + 1-movenum, 0+movenum)
        except:
            pass
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                           for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                         for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                                    for y in range(self.height() - self._padding, self.height() + 1)]




    def mousePressEvent(self, event):
        global imax,allowresize
        # 重写鼠标点击的事件
        #如果允许调整窗体大小，根据鼠标按下位置定义调整大小的部位
        if allowresize==1:
            if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
                # 鼠标左键点击右下角边界区域
                self._corner_drag = True
                event.accept()
            elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
                # 鼠标左键点击右侧边界区域
                self._right_drag = True
                event.accept()
            elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
                # 鼠标左键点击下侧边界区域
                self._bottom_drag = True
                event.accept()
            #最大化时，也允许进入拖动状态，和move互动，发现move就恢复窗口大小模式
            # 最大化时，也允许进入拖动状态，和move互动，发现move就恢复窗口大小模式，这个条件要先执行，不然就执行不到了
            elif (event.button() == Qt.LeftButton) and (event.y() < (self.label.height())) and imax == 1:
                self._maxmove_drag = True
                self._move_drag=True
                event.accept()
            elif (event.button() == Qt.LeftButton) and (event.y() < (self.label.height() + 8)):
                # 鼠标左键点击标题栏区域
                self._move_drag = True
                self.move_DragPosition = event.globalPos() - self.pos()
                event.accept()
        # 最大化时，也允许进入拖动状态，和move互动，发现move就恢复窗口大小模式，这个条件要先执行，不然就执行不到了
        elif (event.button() == Qt.LeftButton) and (event.y() < (self.label.height())) and imax == 1:
            self._maxmove_drag = True
            self._move_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < (self.label.height() + 8)):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()




    def mouseMoveEvent(self, QMouseEvent):
        global imax,allowresize
        if allowresize==1:#如果允许在边角调整大小
            # 判断鼠标位置切换鼠标手势
            if (QMouseEvent.pos() in self._corner_rect and imax==0 and self._move_drag == False):
                self.setCursor(Qt.SizeFDiagCursor)
            elif (QMouseEvent.pos() in self._bottom_rect and imax==0 and self._move_drag == False):
                self.setCursor(Qt.SizeVerCursor)
            elif (QMouseEvent.pos() in self._right_rect and imax==0 and self._move_drag == False):
                self.setCursor(Qt.SizeHorCursor)
            elif(self._corner_drag==True or self._bottom_drag ==True or self._right_drag==True):
                pass
            else:
                self.setCursor(Qt.ArrowCursor)
            # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
            # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
            if (Qt.LeftButton and self._right_drag and imax==0):
                # 右侧调整窗口宽度
                self.resize(QMouseEvent.pos().x(), self.height())
                QMouseEvent.accept()
            elif (Qt.LeftButton and self._bottom_drag and imax==0):
                # 下侧调整窗口高度
                self.resize(self.width(), QMouseEvent.pos().y())
                QMouseEvent.accept()
            elif (Qt.LeftButton and self._corner_drag and imax==0):
                # 右下角同时调整高度和宽度
                self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
                QMouseEvent.accept()


            # 目前是在拖动标题栏时，直接根据鼠标移动位置调整窗体位置，以下两条elif和外面的两条一样
            elif (Qt.LeftButton and self._move_drag and imax == 0):
                # print(self._tomax_drag)
                # 在最大化拖小后重新定位鼠标在窗体按压的位置，居中
                if self._maxmove_drag:
                    self.move_DragPosition = QPoint(self.width() / 2, titleheight / 2)
                    self._maxmove_drag = False
                # 正常拖拽就是鼠标按住哪里就在哪里
                if((QMouseEvent.globalPos().y() == 0 or QMouseEvent.globalPos().x() == 0 or QMouseEvent.globalPos().x() == QDesktopWidget().availableGeometry().right()) and self._tomax_drag==False):
                    # self.setCursor(Qt.SplitHCursor)
                    self._tomax_drag = True
                    #QUnFrameWindow.paintEvent(self, QMouseEvent)
                    self.window().resize(self.width(),self.height()+1)
                    self.window().resize(self.width(), self.height() -1)
                elif (QMouseEvent.globalPos().y() == 0 or QMouseEvent.globalPos().x() == 0 or QMouseEvent.globalPos().x() == QDesktopWidget().availableGeometry().right()):
                    # self.setCursor(Qt.SplitHCursor)
                    self._tomax_drag = True
                elif((QMouseEvent.globalPos().y() == 0 or QMouseEvent.globalPos().x() == 0 or QMouseEvent.globalPos().x() == QDesktopWidget().availableGeometry().right()) and self._tomax_drag==False):
                    # self.setCursor(Qt.SplitHCursor)
                    self._tomax_drag = True
                    #QUnFrameWindow.paintEvent(self, QMouseEvent)
                    self.window().resize(self.width(),self.height()+1)
                    self.window().resize(self.width(), self.height() -1)
                #以上执行完都不符合if条件，代表开始离开边界了
                elif(self._tomax_drag==True):
                    self._tomax_drag = False
                    self.setCursor(Qt.ArrowCursor)
                    #进行调整窗体动作，重绘窗体
                    self.window().resize(self.width(),self.height()+1)
                    self.window().resize(self.width(), self.height() -1)
                self.move(QMouseEvent.globalPos() - self.move_DragPosition)

                QMouseEvent.accept()
            elif (Qt.LeftButton and self._move_drag and imax == 1):  # 针对最大化时拖动标题栏后，窗口恢复正常窗口大小
                self.setCursor(Qt.SizeAllCursor)
                QUnFrameWindow._changeMaxButton(self)
                self.setCursor(Qt.ArrowCursor)
                QMouseEvent.accept()

        # 目前是在拖动标题栏时，直接根据鼠标移动位置调整窗体位置，以下两条和里面的两条一样
        elif (Qt.LeftButton and self._move_drag and imax == 0):
            # 在最大化状态下拖动，拖小后重新定位鼠标在窗体press的位置，居中
            if self._maxmove_drag:
                self.move_DragPosition = QPoint(self.width() / 2, titleheight / 2)
                #关闭最大化拖动开关，已经不再是最大化拖动状态了
                self._maxmove_drag = False

            #此if下都是和鼠标在边界附近时的处理
            # 刚开始拖到边界的时候边界的时候，打开到边界的开关
            if ((QMouseEvent.globalPos().y() == 0 or QMouseEvent.globalPos().x() == 0 or QMouseEvent.globalPos().x() == QDesktopWidget().availableGeometry().right()) and self._tomax_drag == False):
                self._tomax_drag = True
                # 在拖到边界时，调整窗体大小重绘窗体
                self.window().resize(self.width(), self.height() + 1)
                self.window().resize(self.width(), self.height() - 1)
            #已经在边界状态，只要保持边界状态开关一直打开
            elif (QMouseEvent.globalPos().y() == 0 or QMouseEvent.globalPos().x() == 0 or QMouseEvent.globalPos().x() == QDesktopWidget().availableGeometry().right()):
                self._tomax_drag = True
            # 刚开始拖到边界的时候边界的时候，打开到边界的开关
            elif ((QMouseEvent.globalPos().y() == 0 or QMouseEvent.globalPos().x() == 0 or QMouseEvent.globalPos().x() == QDesktopWidget().availableGeometry().right()) and self._tomax_drag == False):
                self._tomax_drag = True
                self.window().resize(self.width(), self.height() + 1)
                self.window().resize(self.width(), self.height() - 1)
            #以上和边界有关的条件都不符合，只有一种情况，是刚开始离开边界，关闭边界开关，重绘窗体阴影
            elif (self._tomax_drag == True):
                self._tomax_drag = False
                self.setCursor(Qt.ArrowCursor)
                self.window().resize(self.width(), self.height() + 1)
                self.window().resize(self.width(), self.height() - 1)
            #正常拖动，在边界状态也是需要拖动的
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()
        elif (Qt.LeftButton and self._move_drag and imax == 1):  # 针对最大化时拖动标题栏后，窗口恢复正常窗口大小
            self.setCursor(Qt.SizeAllCursor)
            QUnFrameWindow._changeMaxButton(self)
            self.setCursor(Qt.ArrowCursor)
            QMouseEvent.accept()





    def mouseReleaseEvent(self, QMouseEvent):

        #拖到上、左、右边界就最大化
        if ((QMouseEvent.globalPos().y()==0 or QMouseEvent.globalPos().x()==0 or QMouseEvent.globalPos().x()==QDesktopWidget().availableGeometry().right()) and self._move_drag==True and imax==0):

            QUnFrameWindow._changeNormalButton(self)

        # 鼠标释放后，各扳机复位,鼠标样式复位
        self._maxmove_drag =False
        self._tomax_drag=False
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self.setCursor(Qt.ArrowCursor)



    #窗口居中
    def center(self):
        qr = self.frameGeometry()  # 获得主窗口的一个矩形特定几何图形。这包含了窗口的框架。
        cp = QDesktopWidget().availableGeometry().center()  # 算出相对于显示器的绝对值。
        # 并且从这个绝对值中，我们获得了屏幕中心点。
        qr.moveCenter(cp)  # 矩形已经设置好了它的宽和高。现在我们把矩形的中心设置到屏幕的中间去。
        # 矩形的大小并不会改变。
        self.move(qr.topLeft())  # 移动了应用窗口的左上方的点到qr矩形的左上方的点，因此居中显示在我们的屏幕

    def _connectJS(self,dict):
        for key,val in dict.items():
            self.webEngineView.page().mainFrame().addToJavaScriptWindowObject(key, val)
            self.webEngineView.page().mainFrame().javaScriptWindowObjectCleared.connect(lambda: self.webEngineView.page().mainFrame().addToJavaScriptWindowObject(key, val))
            # self.webEngineView.page().mainFrame().addToJavaScriptWindowObject(key,val)

    def loadedShow(self):
        self.webEngineView.loadFinished.connect(self.show)

    def startDebugger(self):
        set = self.webEngineView.settings()
        set.setAttribute(QWebSettings.DeveloperExtrasEnabled,True)
        inspector = QWebInspector()
        # inspector.setWindowFlags(Qt.WindowStaysOnTopHint)
        inspector.setPage(self.webEngineView.page())
        self.debugger = inspector

    def runJS(self,js_str):
        return self.webEngineView.page().mainFrame().evaluateJavaScript(js_str)

    def pyConnectJs(self):
        control = Controller()
        self._connectJS({"controller": control})
        db_handler = DataHandler()
        self._connectJS({"db": db_handler})
        file_handler = FileHandler()
        self._connectJS({"file": file_handler})
        doc_handler = docHandler()
        self._connectJS({"doc": doc_handler})

    # 连接前端js和客户端python
    def loadPage(self,htmlstr):
        # self.webEngineView.load(QUrl(url))
        # print(htmlstr)
        self.webEngineView.setHtml(htmlstr)
        self.pyConnectJs()
        self.runJS("__connectLoaded__ && __connectLoaded__()")

        # self.webEngineView.loadFinished.connect(lambda :connector() or callback())

# if __name__ == "__main__":

    # import sys
    # app = QApplication(sys.argv)
    # window = QUnFrameWindow()
    # window.changeinfo('李振飞','机密', '210199292929292212')
    # print(os.path.join("fdsfsd","fsdfsd","fsdfsdfsadf"))
    # os.rmdir("C:/Users/Administrator/Desktop/clientXP/lib/zc/88888")
    # removeDir("C:/Users/Administrator/Desktop/clientXP/lib/zc/88888")

    # window.show()
    #
    # sys.exit(app.exec_())