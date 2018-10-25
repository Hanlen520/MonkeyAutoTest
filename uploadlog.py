#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
    @author:wangzhen
    @contact: zhen.wang@ontim.cn
    @file: uploadlog.py
    @time: 2018-09-04
    @desc:
    """
import os
import platform
from ftplib import FTP
import config
from datetime import datetime


class SyncFiles(object):
    """
    复制本机文件到远端
    """

    def __init__(self):
        self.f = open("existsfile.log", "a+")
        self.remote_host = config.REMOTE_HOST
        self.remote_port = config.REMOTE_PORT
        self.remote_user = config.REMOTE_USER
        self.remote_pwd = config.REMOTE_PWD
        if config.REMOTE_PATH[-1] == '/' or config.REMOTE_PATH[-1] == '\\':
            self.remote_path = config.REMOTE_PATH[0:-1]
        else:
            self.remote_path = config.REMOTE_PATH
        if config.LOCAL_PATH[-1] == '/' or config.LOCAL_PATH[-1] == '\\':
            self.local_path = config.LOCAL_PATH[0:-1]
        else:
            self.local_path = config.LOCAL_PATH

    def get_upload_files(self):
        """获取待上传的所有文件"""
        local_path_set = set()  # 本地文件
        file_transfered_set = set()  # 已经上传过的文件
        for root, dirs, files in os.walk(self.local_path):
            for file in files:
                local_file = os.path.join(root, file)  # 完整的文件路径：/A/B/C/1.txt

                local_path_set.add(local_file)

        print str(local_path_set)
        self.f.seek(0, 0)  # 将记录文件指针放在文件头，用于读文件

        for line in self.f.readlines():
            file_transfered = line.split("-")[-1].strip()

            file_transfered_set.add(file_transfered)

        ready_upload_set = local_path_set ^ file_transfered_set  # 待上传的文件
        return list(ready_upload_set)

    def record_log(self, path):

        now = datetime.now()
        if platform.platform().startswith("Windows"):
            self.f.write(now.strftime('%Y/%M/%d %H:%M:%S %A ') + ' -  ' + path + '\\r\\n')
        else:
            self.f.write(now.strftime('%Y/%M/%d %H:%M:%S %A ') + ' -  ' + path + '\n')


def ftpconnect(host, username, password):
    ftp = FTP()
    encoding = "gbk"
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp


def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024  # 设置缓冲块大小
    ftp.cwd('微农贷')
    fp = open(localpath, 'wb')  # 以写模式在本地打开文件
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)  # 接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)  # 关闭调试
    fp.close()  # 关闭文件


def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)  # 上传文件
    ftp.set_debuglevel(0)
    fp.close()

    # 使用os模块walk函数，搜索出某目录下的全部excel文件
    ######################获取同一个文件夹下的所有excel文件名#######################

def getFileName(filepath):
    file_list = []
    for root, dirs, files in os.walk(filepath):
        for filespath in files:
            # print(os.path.join(root, filespath))
            file_list.append(os.path.join(root, filespath))
    return file_list

def creat_folder():


    pass






    pass


def main():
    ftp = ftpconnect(config.REMOTE_HOST, config.REMOTE_USER, config.REMOTE_PWD)
    filepath = "/home/wangzhen/tmp"
    filelist = getFileName(filepath)
    for each in filelist:
        local = each
        remoute = config.REMOTE_PATH+os.sep+os.path.basename(local)
        uploadfile(ftp, remoute, local)
    ftp.quit()


if __name__ == "__main__":
    main()


