# 解压数据包
import json
import os
import zipfile

from zipencrypt import zipencrypt3
from service.controller.controller import Controller
from service.to_data.dataService import data_service_get
from service.utils import conf, tool
from service.utils.db.db_service import db_get


def unzip(realpath, proKey):
    result = "failed"
    realzip = zipfile.ZipFile(realpath)
    pwd = bytes(proKey, encoding="utf-8")
    try:
        realzip.extractall(conf.data_root(), pwd=pwd)  # 解压到个人目录下
        realzip.close()
        os.remove(realpath)
        result = "hasUnzip"
    except Exception as e:
        print(str(e))
        result = "wrongPwd"
    return result

# 提取数据包MD5值
def get_zipInfo(path, proKey):
    result = False
    try:
        zipf = zipfile.ZipFile(path)

        # 提取md5信息
        zipInfo = str(zipf.comment, encoding="utf-8")
        print('数据包信息MD5：' + zipInfo)

        # 解压文件
        zipf.extractall(conf.data_root())  # 将所有文件解压到lib目录下
        real_zip_path = os.path.join(conf.data_root(), conf.zip_root_name)

        zipInfo = json.loads(zipInfo)

        info_dict = json.loads(tool.decrypt(proKey, zipInfo["info"]))
        print(info_dict)
        result = {"path": real_zip_path, "pro_id": zipInfo["id"], "pro_key": proKey, "info": info_dict}

    except Exception as e:
        print(str(e))
    finally:
        if zipf:
            zipf.close()
    return result


def to_zc_zip(proId, proKey,zipName):
    result = "failed"
    try:
        temp_path = "temp"
        # 数据->压缩包
        dirName = proId
        print("proKey:%s" % proKey)
        data_to_zip(dirName, proKey, temp_path)

        # 添加数据包信息
        md5 = tool.getFileMd5(temp_path)
        print("数据包md5:%s" % str(md5))
        dataInfo = make_zip_head_info(proId, proKey, md5)

        # 压缩包->中存包
        print("压缩包->中存包")
        zip_to_zc(temp_path, zipName, dataInfo)
        os.remove(temp_path)
        result = "success"
    except Exception as e:
        print(str(e))
    return result

def compress_dir(f,files_path,dirName,pwd):
    print("压缩文件%s" % str(files_path))
    pre_len = len(os.path.dirname(files_path))
    for parent, dirnames, filenames in os.walk(files_path):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            files_zip_path = dirName + "/" + arcname
            print('::::%s::::' % files_zip_path)
            f.write(pathfile, files_zip_path, pwd=pwd)
            print('压缩[' + arcname + ']完成！')

def data_to_zip(dirName, proKey, to_path):
    pwd = bytes(proKey, encoding="utf-8")
    with zipencrypt3.ZipFile(to_path, mode="w") as f:
        # 1.打包上传的附件
        files_path = conf.upfile_path()
        compress_dir(f,files_path,dirName,pwd)

        # 2.打包数据库文件
        db_path = conf.db_path()
        print("压缩数据库%s" % str(db_path))
        db_zip_path = os.path.join(dirName, conf.zip_db_path)
        f.write(db_path, db_zip_path, pwd=pwd)

        # 3.打包html前端资源
        html_path = conf.page_root()
        compress_dir(f,html_path,dirName,pwd)

        # 4.打包word模板
        word_path = conf.word_path()
        print("压缩word%s" % str(word_path))
        word_zip_path = os.path.join(dirName, "word/default.docx")
        f.write(word_path, word_zip_path, pwd=pwd)

def zip_to_zc(src_path, to_path, info):
    if not to_path.endswith(".zc"):
        to_path = to_path + ".zc"
    print("---1------")
    with zipencrypt3.ZipFile(to_path, mode="w") as f:
        print("-------2--------")
        f.write(src_path, conf.zip_root_name)
        f.comment = bytes(json.dumps(info), encoding="utf-8")

        print('数据包信息：' + str(f.comment, encoding="utf-8"))
        print("------------------------------------------")


# 组织数据包头信息
def make_zip_head_info(proId, proKey, md5):
    result = {}
    applyInfo = db_get("select * from apply where id='%s'" % str(proId))
    if applyInfo:
        # result['apply_id'] = applyInfo['id']
        result['md5'] = md5
        result['company_name'] = tool.decrypt(proKey, applyInfo['company_name'])
        result['apply_date'] = applyInfo['apply_date']
        result["evalname"] = tool.decrypt(proKey, applyInfo["evalname"])
        result["update_date"] = applyInfo["update_date"]
        result["proxy"] = applyInfo["proxy"]
        result["proxy_contact"] = applyInfo["proxy_contact"]
        result["pro_id"] = applyInfo['pro_id']

    return {"id": proId, "info": tool.encrypt(proKey, json.dumps(result))}


def unzip_zc_zip(zipName, proId, proKey):
    result = "failed"
    try:
        if os.path.isfile(zipName):
            zipInfo = get_zipInfo(zipName, proKey)

            print('2-数据包信息MD5：%s' % str(zipInfo))
            if zipInfo:
                realpath = zipInfo["path"]
                calcMd5 = str(tool.getFileMd5(realpath))
                print('数据包计算MD5：' + calcMd5)
                if calcMd5 == zipInfo["info"]['md5']:
                    result = unzip(realpath, proKey)
                    print("解压下载数据包的结果：%s" % str(result))
                    if result == "hasUnzip":
                        srcPath = os.path.join(conf.data_root(), proId)
                        tool.extractDir_toDir(srcPath, conf.data_root())

                        apply = data_service_get("apply", {"pro_id": zipInfo['pro_id']}, zipInfo['pro_key'])
                        if apply:
                            Controller.render_apply_page(apply)
                else:
                    result = "noEqual"
    except Exception as e:
        result = "failed"
        print(str(e))

    return result
