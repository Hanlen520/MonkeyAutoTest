#!/usr/bin/env python
# coding=utf-8

"""

@author: wangzhen

@contact: zhen.wang@ontim.cn

@file: monkeyTest.py

@time: 18-5-31 下午4:26

@desc:Excute Monekey and getlogs

"""

import Queue
import os
import time
import threading
import getResult
from xml.dom.minidom import parse
import xml.dom.minidom
import Email
import config

# globle var
anlayze_result = []


# get current path
def getfilePath():
    return os.getcwd() + os.sep


# get RAM
def getRAM(sn):
    print('get RAM ...')
    process = os.popen('adb -s %s shell cat /proc/meminfo' % sn)  # return file
    output = process.readline()
    ramsize = float(output.split()[1]) / 1000 / 1000
    process.close()
    if 1.7 < ramsize < 2.1:
        return '2G'
    if 0.8 < ramsize < 1.2:
        return '1G'


# get SN
def getSN():
    sn = os.getenv("SN")
    if sn == None:
        return None
    else:
        return sn


# excute monkey

def excutemonkey(tag, sn, pack, testduration, white_flag, black_flag, BLACK_LIST, WHITE_LIST, event):
    throttleTime = 1000
    tombstone = "/data/tombstones"
    localtimemonkey = time.strftime('%H_%M_%S', time.localtime(time.time()))
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    monlogpath = getfilePath() + "MonkeyLog" + os.sep
    # monlogpathdate = monlogpath + local_date + os.sep
    monlogmodel = monlogpath + pack + os.sep
    devicepath = monlogmodel + tag + os.sep
    os.system("adb -s %s remount" % sn)
    os.system("adb -s %s shell rm remount" % sn)
    os.system("adb -s %s shell rm -rf /data/tombstones" % sn)
    os.system("adb -s %s shell rm -rf /data/system/dropbox" % sn)
    os.system("adb -s %s shell mkdir /data/tombstones" % sn)
    os.system("adb -s %s shell mkdir /data/system/dropbox" % sn)
    if not os.path.exists(monlogpath):
        os.system('mkdir %s' % (monlogpath))
    # if not os.path.exists(monlogpathdate):
    # 	os.system('mkdir %s' % (monlogpathdate))
    if not os.path.exists(monlogmodel):
        os.system('mkdir %s' % (monlogmodel))
    if not os.path.exists(devicepath):
        os.mkdir(devicepath)
    ram = getRAM(sn)
    if testduration == 0:
        testduration = 6
    else:
        pass

    print(str(testduration))
    if ram == '1G':
        throttleTime = 700
        eventCount = int(1000000 / 6 / 7 * float(testduration))
    if ram == '2G':
        throttleTime = 400
        eventCount = int(250000 / 6 * float(testduration))
    print("black_flag: " + str(black_flag))
    print("white_flag: " + str(white_flag))
    if pack == "monkey":
        print("eventCount :" + str(eventCount))
        if black_flag:
            print("excute monkey with black list")
            os.system("adb -s %s push %s /sdcard/%s" % (sn, BLACK_LIST, BLACK_LIST))
            os.remove(BLACK_LIST)
            sdcardfile = '/sdcard/%s' % BLACK_LIST
            monkeyorder = "adb -s %s shell monkey --pkg-blacklist-file %s --throttle %d -c " \
                          "android.intent.category.LAUNCHER -c " \
                          "android.intent.category.MONKEY -c android.intent.category.DEFAULT -c " \
                          "android.intent.category.BROWSABLE -c android.intent.category.TAB -c " \
                          "android.intent.category.ALTERNATIVE -c android.intent.category.SELECTED_ALTERNATIVE -c" \
                          " android.intent.category.INFO -c android.intent.category.HOME -c" \
                          " android.intent.category.PREFERENCE -c android.intent.category.TEST -c " \
                          "android.intent.category.CAR_DOCK -c android.intent.category.DESK_DOCK -c " \
                          "android.intent.category.CAR_MODE  --ignore-security-exceptions --ignore-timeouts" \
                          " --ignore-crashes --ignore-native-crashes --monitor-native-crashes -v -v -v %d " \
                          "> %s%s_%s_%s.txt 2>&1" % (
                              sn, sdcardfile, throttleTime, eventCount, devicepath, pack, sn[-6:], localtimemonkey)
        elif white_flag:
            print("in excute contains whitelist")
            os.system("adb -s %s push %s /sdcard/%s" % (sn, WHITE_LIST, WHITE_LIST))
            os.remove(WHITE_LIST)
            sdcardfile = '/sdcard/%s' % WHITE_LIST
            monkeyorder = "adb -s %s shell monkey --pkg-whitelist-file %s --throttle %d -c " \
                          "android.intent.category.LAUNCHER -c " \
                          "android.intent.category.MONKEY -c android.intent.category.DEFAULT -c " \
                          "android.intent.category.BROWSABLE -c android.intent.category.TAB -c " \
                          "android.intent.category.ALTERNATIVE -c android.intent.category.SELECTED_ALTERNATIVE -c" \
                          " android.intent.category.INFO -c android.intent.category.HOME -c" \
                          " android.intent.category.PREFERENCE -c android.intent.category.TEST -c " \
                          "android.intent.category.CAR_DOCK -c android.intent.category.DESK_DOCK -c " \
                          "android.intent.category.CAR_MODE  --ignore-security-exceptions --ignore-timeouts" \
                          " --ignore-crashes --ignore-native-crashes --monitor-native-crashes -v -v -v %d " \
                          "> %s%s_%s_%s.txt 2>&1" % (
                              sn, sdcardfile, throttleTime, eventCount, devicepath, pack, sn[-6:], localtimemonkey)
        else:

            monkeyorder = "adb -s %s shell monkey --throttle %d -c android.intent.category.LAUNCHER -c " \
                          "android.intent.category.MONKEY -c android.intent.category.DEFAULT -c " \
                          "android.intent.category.BROWSABLE -c android.intent.category.TAB -c " \
                          "android.intent.category.ALTERNATIVE -c android.intent.category.SELECTED_ALTERNATIVE -c" \
                          " android.intent.category.INFO -c android.intent.category.HOME -c" \
                          " android.intent.category.PREFERENCE -c android.intent.category.TEST -c " \
                          "android.intent.category.CAR_DOCK -c android.intent.category.DESK_DOCK -c " \
                          "android.intent.category.CAR_MODE  --ignore-security-exceptions --ignore-timeouts" \
                          " --ignore-crashes --ignore-native-crashes --monitor-native-crashes -v -v -v %d " \
                          "> %s%s_%s_%s.txt 2>&1" % (
                              sn, throttleTime, eventCount, devicepath, pack, sn[-6:], localtimemonkey)
    else:

        monkeyorder = "adb -s %s shell monkey -p %s --throttle %d -c android.intent.category.LAUNCHER -c " \
                      "android.intent.category.MONKEY -c android.intent.category.DEFAULT -c " \
                      "android.intent.category.BROWSABLE -c android.intent.category.TAB -c " \
                      "android.intent.category.ALTERNATIVE -c android.intent.category.SELECTED_ALTERNATIVE -c" \
                      " android.intent.category.INFO -c android.intent.category.HOME -c" \
                      " android.intent.category.PREFERENCE -c android.intent.category.TEST -c " \
                      "android.intent.category.CAR_DOCK -c android.intent.category.DESK_DOCK -c " \
                      "android.intent.category.CAR_MODE  --ignore-security-exceptions --ignore-timeouts" \
                      " --ignore-crashes --ignore-native-crashes --monitor-native-crashes -v -v -v %d " \
                      "> %s%s_%s_%s.txt 2>&1" % (
                          sn, pack, throttleTime, eventCount, devicepath, pack, sn[-6:], localtimemonkey)

    print('excuting %s monkey test...' % pack.split('.')[-1])
    print ("monkeyorder =" + monkeyorder)
    err = os.system(monkeyorder)
    print("back:" + str(err))
    event.set()
    path = "%s%s_%s_%s.txt" % (devicepath, pack, sn[-6:], localtimemonkey)
    return path


# transfer time to second
def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec


# power off mobile phone
def poweroff(sn):
    os.system("adb -s %s shell reboot -p" % sn)


# reboot mobile phone
def rebootdut(sn):
    os.system("adb -s %s shell reboot" % sn)


# close MTK log
def closelog(sn):
    os.system(
        "adb -s %s shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name stop --ei cmd_target 7" % sn)
    time.sleep(10)


# open mtk log
def openlog(sn):
    print("open mtklog ...")
    os.system("adb -s %s shell settings put system screen_off_timeout 1800000" % sn)
    print('set screen on time')
    # os.system("adb -s %s shell pm clear com.mediatek.mtklogger" % sn)
    os.system("adb -s %s shell am start -n com.mediatek.mtklogger/com.mediatek.mtklogger.MainActivity" % sn)
    time.sleep(20)
    os.system(
        "adb -s %s shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name switch_taglog --ei cmd_target  1" % sn)
    os.system(
        "adb -s %s shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name set_auto_start_1 --ei cmd_target 7" % sn)
    os.system(
        "adb -s %s shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name start --ei cmd_target 1" % sn)
    time.sleep(10)
    os.system("adb -s %s shell input keyevent 3" % sn)
    time.sleep(10)


# clear all logs after pull
def clearlogs(sn):
    os.system('adb -s %s root' % sn)
    os.system('adb -s %s remount' % sn)
    time.sleep(5)
    # os.system('adb -s %s shell rm -rf /sdcard/mtklog/'%sn)
    os.system('adb -s %s shell rm -rf /data/aee_exp/*' % sn)
    os.system('adb -s %s shell rm -rf /data/vendor/mtklog/aee_exp/*' % sn)
    os.system('adb -s %s shell rm -rf /data/log/*' % sn)
    os.system('adb -s %s shell rm -rf /data/system/dropbox/*' % sn)
    os.system('adb -s %s shell rm -rf /data/tombstones/*' % sn)
    os.system('adb -s %s shell rm -rf /log/*' % sn)
    os.system('adb -s %s shell rm -rf /data/anr/*' % sn)
    os.system('adb -s %s shell rm -rf /sys/fs/pstore/*' % sn)


# stop runing monkey
def stopmonkey(sn):
    print('stoping monkey...')
    os.system('adb -s %s shell ps -A >ps.txt' % sn)
    psfile = 'ps.txt'
    file_object = open(psfile)
    try:
        file_context = file_object.readline()
        while not file_context == '':
            if "monkey" in file_context:
                print("monkey is killing")
                pid = file_context.split()[1]
                os.system("adb -s %s shell kill -9 %s " % (sn, pid))
            file_context = file_object.readline()
    finally:
        file_object.close()
        os.remove(psfile)


def checkappinstalled(sn, pack):
    os.system("adb -s %s shell pm -l >%s_app.txt" % (sn, sn))
    appfile = sn + '_app.txt'
    flag = False
    Installedapk = []
    for i in range(len(pack)):
        print(str(i) + " : " + pack[i])

    try:
        file_object = open(appfile)
        file_context = file_object.readline().strip()
        while not file_context == "":
            for app in pack:
                if app == file_context.split(':')[1].strip():
                    Installedapk.append(app)
            file_context = file_object.readline().strip()

    finally:
        file_object.close()
        os.remove(appfile)
    print "%s :installed apk" % sn
    print list(Installedapk)
    if len(Installedapk) == len(pack):
        flag = True
    else:
        NotInstalledApk = set(pack).difference(Installedapk)
        print('\n%s Apk not installed' % sn)
        print('**' * 10)
        print list(NotInstalledApk)
        print('**' * 10)
        flag = False
    return flag


def get_file_size(filePath):
    fsize = os.path.getsize(filePath)
    return fsize


# full all logs function
def pull_all_logs(sn, pack, tag):
    # stopmonkey(sn)
    # print('stop log...')
    # closelog(sn)
    print('pulling logs...')
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    local_time = time.strftime('%H_%M_%S', time.localtime(time.time()))
    logpath1 = getfilePath() + 'AllLog' + os.sep
    # logpathdir = logpath1 + local_date + os.sep
    logpathmodel = logpath1 + pack + os.sep
    logdevice = logpathmodel + tag + os.sep
    logpath = logdevice + 'log_' + sn[:6] + '_' + local_time + os.sep
    if not os.path.exists(logpath1):
        os.system('mkdir %s' % logpath1)
    # if not os.path.exists(logpathdir):
    # 	os.system('mkdir %s' % logpathdir)
    if not os.path.exists(logpathmodel):
        os.system('mkdir %s' % logpathmodel)
    if not os.path.exists(logdevice):
        os.mkdir(logdevice)
    if not os.path.exists(logpath):
        os.system('mkdir %s' % (logpath))
    os.system('adb -s %s root' % sn)
    os.system('adb -s %s remount' % sn)
    # os.system('mkdir %smtklog' % (logpath))
    # os.system('adb -s pull /sdcard/mtklog %smtklog' % (sn, logpath))
    time.sleep(5)
    os.system('mkdir %sdata_aee_exp' % (logpath))
    os.system('adb -s %s pull /data/aee_exp %sdata_aee_exp' % (sn, logpath))
    os.system('mkdir %sdata_vendor_mtklog_aee_exp' % (logpath))
    os.system('adb -s %s pull /data/vendor/mtklog/aee_exp %sdata_vendor_mtklog_aee_exp' % (sn, logpath))
    os.system('mkdir %sdata_log' % (logpath))
    os.system('adb -s %s pull /data/log %sdata_log' % (sn, logpath))
    os.system('mkdir %sdropbox' % (logpath))
    os.system('adb -s %s pull /data/system/dropbox %sdropbox' % (sn, logpath))
    os.system('mkdir %sdata_tombstone' % (logpath))
    os.system('adb -s %s pull /data/tombstones %sdata_tombstone' % (sn, logpath))
    os.system('mkdir %slog' % (logpath))
    os.system('adb -s %s pull /log %slog' % (sn, logpath))
    os.system('mkdir %sdata_anr' % (logpath))
    os.system('adb -s %s pull /data/anr %sdata_anr' % (sn, logpath))
    os.system('mkdir %spstore' % (logpath))
    os.system('adb -s %s pull /sys/fs/pstore %spstore' % (sn, logpath))
    os.system('adb -s %s shell "getprop ro.versions.internal_sw_ver" >%sversion.txt' % (sn, logpath))


# excute monkey Thread
class ExcuteMonkeyThread(threading.Thread):
    def __init__(self, name, device, q, pack, testduration, white_flag, black_flag, BLACK_LIST, WHITE_LIST, eventi):
        threading.Thread.__init__(self)
        self.name = name
        self.pack = pack
        self.device = device
        self.sn = self.device[1]
        self.tag = self.device[0]
        self.WHITE_LIST = WHITE_LIST
        self.BLACK_LIST = BLACK_LIST
        print(self.name + " is running")
        self.testduration = testduration
        self.q = q
        self.eventi = eventi
        self.white_flag = white_flag
        self.black_flag = black_flag

    def run(self):
        logpath = excutemonkey(self.tag, self.sn, self.pack, self.testduration, self.white_flag, self.black_flag,
                               self.BLACK_LIST, self.WHITE_LIST, self.eventi)
        self.q.put(logpath)
        return True

    # pull log Thread


class PullLogThread(threading.Thread):
    def __init__(self, name, device, logInterval, pack, eventi):
        threading.Thread.__init__(self)
        self.name = name
        self.logInterval = logInterval
        self.pack = pack
        self.sn = device[1]
        self.tag = device[0]
        self.eventi = eventi
        print(self.name + " is running")

    def run(self):
        print("event.isSet:" + str(self.eventi.isSet()))
        exitflag = False
        print("self.logInterval = " + self.logInterval)
        varInter = int(self.logInterval)
        if varInter == 0:
            varInter = 7200
        else:
            pass
        print("varInter :" + str(varInter))
        while not self.eventi.isSet():
            pull_all_logs(self.sn, self.pack, self.tag)
            print "waitting-for-logInterval :%ss" % str(varInter)
            for i in range(1, 10, 1):
                if not self.eventi.isSet():
                    print("waiting %d s check loop : %d " % (varInter / 10, i))
                    time.sleep(varInter / 10)
                else:
                    exitflag = True
                    break
            if exitflag:
                break
        pull_all_logs(self.sn, self.pack, self.tag)


# wake up mobilephone
def wakeup(sn):
    # os.system('adb -s %s shell input keyevent 26'%sn)
    print("in wake up")
    os.system('adb -s %s shell input keyevent 224' % sn)
    os.system('adb -s %s shell input swipe 500 700 500 50 50' % sn)


def creat_file(filepath, content):
    print("creat files")
    print(filepath)
    if os.path.exists(filepath):
        os.system("rm %s" % filepath)
    text = open(filepath, 'a+')
    contents = content.split(';')
    for con in contents:
        text.write(con + '\n')
    text.close()


def get_paraments():
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("plan.xml")
    collection = DOMTree.documentElement
    # if collection.hasAttribute("shelf"):
    #     print "Root element : %s" % collection.getAttribute("shelf")

    # 获取所有集合中的model
    models = collection.getElementsByTagName("phone")

    re = []
    print "*****phone info*****"
    # 打印每个测试的信息
    for model in models:
        tag_con = ''
        sn_con = ''
        whitelist_con = ''
        blacklist_con = ''
        package_con = ''
        duration = ''
        interval = ''

        tag = model.getElementsByTagName("tag")
        if not tag == []:
            tag_con = tag[0].childNodes[0].data
        sn_con = model.getAttribute('SN')
        whitelist = model.getElementsByTagName('whitelist')
        if not whitelist[0].childNodes == []:
            whitelist_con = whitelist[0].childNodes[0].data.strip()
        blacklist = model.getElementsByTagName('blacklist')
        if not blacklist[0].childNodes == []:
            blacklist_con = blacklist[0].childNodes[0].data.strip()
        package = model.getElementsByTagName('package')
        if not package[0].childNodes == []:
            package_con = package[0].childNodes[0].data.strip()
            if ';' in package_con:
                package_con = package_con.split(';')
            else:
                package_con = [package_con]
        testduration = model.getElementsByTagName('testduration')
        if not testduration[0] == []:
            duration = testduration[0].childNodes[0].data.strip()
        loginterval = model.getElementsByTagName('loginterval')
        if not loginterval[0] == []:
            interval = loginterval[0].childNodes[0].data.strip()

        re.append([tag_con, sn_con, whitelist_con, blacklist_con, package_con, duration, interval])

    return re


def foreachdevice(device, eventi, q):
    print(device[0])
    packageName = []
    white_list = []
    black_list = []
    global white_flag
    global black_flag
    logInterval = 0
    testduration = 0

    if not device[4] == '':
        packageName = device[4]
        print("packageName : " + str(packageName))
    sn = device[1]
    if not device[2] == '':
        white_list = device[2]
    if not device[3] == '':
        black_list = device[3]
    if not device[5] == '':
        testduration = device[5]
    if not device[6] == '':
        logInterval = device[6]
    WHITE_LIST = 'whitelist%s.txt' % sn[-6::]
    BLACK_LIST = 'blacklist%s.txt' % sn[-6::]

    if not white_list == []:
        creat_file(os.getcwd() + os.sep + WHITE_LIST, white_list)
        white_flag = True
    else:
        white_flag = False
    if not black_list == []:
        creat_file(os.getcwd() + os.sep + BLACK_LIST, black_list)
        black_flag = True
    else:
        black_flag = False

    if not (white_flag and black_flag):
        if not len(packageName) == 0:
            if checkappinstalled(sn, packageName):
                for pack in packageName:
                    os.system('adb -s %s wait-for-device' % sn)
                    wakeup(sn)
                    eventi.clear()
                    # excute monkey test Thread
                    t1 = ExcuteMonkeyThread('excuteMonkey', device, q, pack, testduration, white_flag, black_flag,
                                            BLACK_LIST, WHITE_LIST, eventi)
                    t1.start()
                    # sleep wait for end of monkey Thread
                    print "logInterval before excute = " + str(logInterval)
                    t2 = PullLogThread('pullLog', device, logInterval, pack, eventi)
                    if t1.is_alive():
                        t2.start()
                        t2.join()
                    else:
                        print("Monkey is not Running,please confirm")
                        os._exit(1)
                    t1.join()
                    if not q.empty():
                        logfile = q.get()
                    print("logfile = " + logfile)
                    print "t2,isalive:" + str(t2.isAlive())
                    print("============================= %s monkey test finished =============================" % (
                        pack))
                    clearlogs(sn)
                    testInfo = getResult.getusefulInfo(logfile)
                    anlayze_result.append(testInfo)
                    print "testInfo = " + str(testInfo)

                    time.sleep(sleeptime(0, 3, 0))
            else:
                print(
                    "============================= monkey test failed,part of apk is not installed "
                    "=============================")
                os._exit(1)
        else:
            os.system('adb -s %s wait-for-device' % sn)
            print("get SN")
            wakeup(sn)
            eventi.clear()
            # excute monkey test Thread
            t1 = ExcuteMonkeyThread('excuteMonkey', device, q, "monkey", testduration, white_flag, black_flag,
                                    BLACK_LIST,
                                    WHITE_LIST, eventi)
            t1.start()
            # sleep wait for end of monkey Thread
            print "logInterval before excute = " + str(logInterval)
            t2 = PullLogThread('pullLog', device, logInterval, "monkey", eventi)
            if t1.is_alive():
                t2.start()
                t2.join()
            else:
                print("Monkey is not Running,please confirm")
                os._exit(1)
            t1.join()
            if not q.empty():
                logfile = q.get()
            print("log file = " + logfile)
            print "t2,isalive:" + str(t2.isAlive())
            os.system("adb -s %s shell input keyevent 3" % sn)
            testInfo = getResult.getusefulInfo(logfile)
            anlayze_result.append(testInfo)
            print "testInfo = " + str(testInfo)
            time.sleep(sleeptime(0, 1, 0))
        # power off
        poweroff(sn)

        print("============================= %s : All Test Finished =============================" % sn)
    else:
        print "it is not allowed to config both black list and white list in one device"
        if os.path.exists(os.getcwd() + os.sep + BLACK_LIST):
            os.remove(os.getcwd() + os.sep + BLACK_LIST)
        if os.path.exists(os.getcwd() + os.sep + WHITE_LIST):
            os.remove(os.getcwd() + os.sep + WHITE_LIST)


def get_sn():
    sns = []
    cmd = os.popen("adb devices")
    line = cmd.readline()
    while not line == "":

        content = str(line)
        if content.startswith("List"):
            line = cmd.readline().strip()
            continue
        else:
            status = content.split('\t')[1]
            sn = content.split('\t')[0]
            # print(status)
            if status == 'device':
                sns.append(sn)
        line = cmd.readline().strip()
    return sns


def check_device(para):
    devices = get_sn()
    for device in devices:
        for sn in para:
            if device == sn[1]:
                para.remove(sn)
            else:
                pass
    return para


def get_dut_info(sn):
    ret = []
    version = os.popen('adb -s %s shell "getprop|grep sw_ver"' % sn).read().split(':')[1].strip().strip('[').strip(']')
    model = os.popen('adb -s %s shell "getprop|grep ro.product.name"' % sn).read().split(':')[1].strip().strip(
        '[').strip(']')
    ret.append(version)
    ret.append(model)
    # ret.append(vendor_country)
    return ret


def email_content():
    duts = get_paraments()
    info = []
    for dut in duts:
        ret = get_dut_info(dut[1])
        dut.extend(ret)
        info.append(dut)
    return info


class ForeachDevice(threading.Thread):
    def __init__(self, device, event, q):
        threading.Thread.__init__(self)
        self.device = device
        self.eventi = event
        self.q = q

    def run(self):
        foreachdevice(self.device, self.eventi, self.q)


if __name__ == '__main__':
    che_res = check_device(get_paraments())
    para = get_paraments()
    mes = u''
    email_string = u''
    content = email_content()
    if len(che_res) == 0:
        for dut in para:
            event_i = threading.Event()
            qi = Queue.Queue()
            ti = ForeachDevice(dut, event_i, qi)
            ti.start()
        for j in range(len(para)):
            ti.join()
        mes = u"test finished \n \n \nMonkeyAutotest , No need to reply\nMonkey测试结果，不需回复此邮件"

    else:
        for dev in che_res:
            print dev[0] + " is not founded ..."
        mes = u"Some device Not Founded \n \n \n No need to reply\nMonkey测试结果，不需回复此邮件"
    print "mes = " + mes

    for tag in anlayze_result:
        for j in content:
            if tag[0] == j[0]:
                j.extend(tag[1::])

    for i in range(len(content)):
        email_string += u"\nModel: %s \nTAG: %s\nSN: %s\nVersion: %s \nWhite List: %s\nBlack List: %s \nPackage: %s " \
                        u"\nTest Duration: %sh\nLogInterval: %ss \n\nStart Time: %s\nEnd Time: %s\nRun Time: %sh%sm%ss\n\n\n" \
                        % (content[i][8], content[i][0], content[i][1], content[i][7], content[i][2], content[i][3],
                           content[i][4], content[i][5], content[i][6], content[i][9], content[i][10],
                           content[i][11][0],
                           content[1][11][1], content[1][11][2])
    print "email_string = " + email_string
    email = Email.Email(u"自动化Monkey测试", config.RECEIVE_EMAIL_ADDR, email_string + mes)
    email.send_email()
    # email_string = ''
    # logfile1 = "/home/wangzhen/monkeyAutoTest/MonkeyLog/com.android.contacts/L0317#/com.android.contacts_D00903_13_50_04.txt"
    # logfile2 = "/home/wangzhen/monkeyAutoTest/MonkeyLog/com.huawei.android.launcher/L0320#/com.huawei.android.launcher_900909_13_50_04.txt"
    #
    # testInfo = getResult.getusefulInfo(logfile1)
    # anlayze_result.append(testInfo)
    # testInfo = getResult.getusefulInfo(logfile2)
    # anlayze_result.append(testInfo)
    # content = email_content()
    # for tag in anlayze_result:
    #     for j in content:
    #         if tag[0] == j[0]:
    #             j.extend(tag[1::])
    # print content
    # print "length = "+str(len(content))
    # for i in range(len(content)):
    #     email_string += u"\nModel: %s \nTAG: %s\nSN: %s\nVersion: %s \nWhite List: %s\nBlack List: %s \nPackage: %s " \
    #                     u"\nTest Duration: %sh\nLogInterval: %ss \n\nStart Time: %s\nEnd Time: %s\nRun Time: %sh%sm%ss\n\n\n"\
    #                     % (content[i][8], content[i][0], content[i][1], content[i][7], content[i][2], content[i][3],content[i][4]
    #                     , content[i][5], content[i][6],content[i][9],content[i][10],content[i][11][0],content[1][11][1],content[1][11][2])
    # print "email_string = " + email_string
    # email = Email.Email(u"自动化Monkey测试结果", config.RECEIVE_EMAIL_ADDR, email_string)
    # email.send_email()
