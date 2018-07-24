import os
import winreg

import datetime
from service.utils import tool

from service.utils.tool import transPath

'''
客户端设置
'''
apptitle = "测评风评数据管理系统"
webkiturl = 'qrc:/index.html'
titleheight = 80
infobgimgwidth = 230
infotopwidth = 25  # 信息区的顶部留空高度
infoIndent = 40  # 信息区文字缩进
infofont = '微软雅黑'
appicon = ':/EDM.ico'
infobgimg = ":/img/infobg.png"
titleimg = ":/img/title.png"
windowminW = 916  # 窗体最小宽度
windowminH = 600  # 窗体最小高度
qssfile = ":/EDM.qss"


# 获取桌面路径
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


# 窗口大小
app_width = 980
app_height = 600
# 最小宽高
app_min_width = 980
app_min_height = 600

# 项目数据库的明文字段
pro_no_secrets = ['id', 'apply_date', 'apply_id']

# 窗口标题
win_title = "测评申请书"


# 压缩文件源文件夹
# zip_source = 'lib/files';
# 压缩目标文件
@transPath
def zip_target():
    return os.path.join(get_desktop(), zip_file_name())


def zip_file_name():
    return 'data_%s.zc' % str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))


# 压缩包文件类型
zip_type = 'ZC Files (*.zc)'

# doc导出默认路径
doc_path = get_desktop() + '/测评申请书.doc'
doc_type = "Doc Files (*.doc)"


# 数据库文件路径
@transPath
def db_path():
    return os.path.join(data_root(), "data/data.db")


# 打包后的数据库文件路径
zip_db_path = "data/data.db"


# 上传文件存放路径
@transPath
def upfile_path():
    return os.path.join(data_root(), "files")


# 选择上传文件的类型
selectfile_type = 'All Files (*);'
# 选择上传文件的默认打开地址
selectfile_path = get_desktop()

# app_path = ""


# 数据文件的根目录
@transPath
def data_root():
    return "lib/"
    # return os.path.join(app_path, "lib/")


@transPath
def page_root():
    return os.path.join(data_root(), "page")


@transPath
def html_path_to_zip():
    return os.path.join(page_root(), "main.zc")


@transPath
def word_path():
    return os.path.join(data_root(), "word/default.docx")


@transPath
def login_page_path():
    # return "C:/Users/Administrator/Desktop/test.html"
    return os.path.join(page_root(), "login.html")
    # return "lib/page/login.html"

@transPath
def main_page_path():
    return os.path.join(page_root(), "main.html")

zip_root_name = "zcsoft"

webView = ""

local_key = "A1225"

# 与服务器通信秘钥
# server_key = "868608"


