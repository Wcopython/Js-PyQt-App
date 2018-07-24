import base64
import hashlib

import os
import shutil

import time
from Cryptodome.Cipher import AES

'''
采用AES对称加密算法
'''


# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


# 加密方法
def encrypt(key, text):
    result = ''
    if text:
        try:
            text = base64.encodebytes(text.encode('utf-8'))
            text = str(text, 'utf-8')
            aes = AES.new(add_to_16(key), AES.MODE_ECB)
            # 先进行aes加密
            encrypt_aes = aes.encrypt(add_to_16(text))
            # 用base64转成字符串形式
            result = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        except:
            result = text
    return result.replace("\n", "")


# 解密方法
def decrypt(key, text):
    result = ''
    if text:
        try:
            # 初始化加密器
            aes = AES.new(add_to_16(key), AES.MODE_ECB)
            # 优先逆向解密base64成bytes
            base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
            #
            decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8')  # 执行解密密并转码返回str

            result = str(base64.b64decode(decrypted_text), 'utf-8')
        except:
            result = text

    return result


def decrypt_db_val(serialId, records, no_secret_field):
    arr = []
    for row in records:
        dict = {}
        for key in row.keys():
            dict[key] = row[key] if key in no_secret_field else decrypt(serialId, row[key])
        arr.append(dict)
    return arr


# 新增记录加密字段
def encrypt_db_val(key, dict, no_secret_field):
    for k in dict:
        if (k not in no_secret_field):
            dict[k] = encrypt(key, dict[k])


# 计算文件md5值
def getFileMd5(filepath):
    if not os.path.isfile(filepath):
        return
    myhash = hashlib.md5()
    f = open(filepath, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def removeDir(dir):
    filelist = os.listdir(dir)
    for f in filelist:
        filepath = os.path.join(dir, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(filepath + " removed!")
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
            print("dir " + filepath + " removed!")
    os.rmdir(dir)


def extractDir_toDir(srcDir, toDir):
    filelist = os.listdir(srcDir)
    for f in filelist:
        srcFile = os.path.join(srcDir, f)
        toFile = os.path.join(toDir, f)
        if os.path.isfile(srcFile):
            shutil.copy(srcFile, toFile)
        elif os.path.isdir(srcFile):
            shutil.rmtree(toFile)
            shutil.copytree(srcFile, toFile)
    shutil.rmtree(srcDir)

def readHtml(path):
    with open(path, mode='r', encoding='UTF-8') as file:
        content = file.read()
    return content

def readHtmlByKey(path,key):
    content = readHtml(path)
    return decrypt(key,content)

def get_now_time():
    return str(round(time.time() * 1000))

def transPath(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.replace("\\","/") if result else ""
    return inner


if __name__ == "__main__":
     with open("C:/Users/Administrator/Desktop/EDM/填报端/lib/page/dist/main.html", mode='r', encoding='UTF-8') as file_object:

        contents = file_object.read()
        with open("C:/Users/Administrator/Desktop/EDM/填报端/lib/page/dist/main_dist.html","w") as f:
            f.write(encrypt("123456",contents))
    # file = open()
    # a = encrypt('123456', '''分级保护测评''')
    # b = decrypt("868608",
    #             "Yiolp2Kh1kdSq3RahVch5inOjk8dAiugZo/Cn6tx29TvOfJQGQlSiGlwBgtIG9UM7r88Uvi6UDRNgUuZ9eayRXGg4ZLELDq3bpWz4AGNmqo=")
    # b = getFileMd5("C:/Users/Administrator/Desktop/files.zc")
    # print(decrypt('1',"5YWs5byA\n"))
    # print(a)
    # print(os.path.pardir("/a/b/c.txt"))
