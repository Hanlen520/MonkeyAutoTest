#!/usr/bin/env python
# coding=utf-8

"""

@author: wangzhen

@contact: zhen.wang@ontim.cn

@file: getResult.py

@time: 18-5-31 下午4:26

@desc:analyse monkey log to generate report of monkey test

"""
import re
import linecache
import os
import shutil


def timeShift(time):
    h = int(time / 3600000)
    m = int((time / 60000 - h * 60))
    s = int((time / 1000 - h * 3600 - m * 60))
    return h, m, s


def getusefulInfo(logfile):
    ret = []
    if os.path.exists(logfile):
        print('Analysing Results After monkey excute...')
        file_path = os.path.dirname(logfile) + os.sep
        file_name = os.path.split(logfile)[-1]
        curfol = os.path.join(file_path, file_name.strip('.txt'))
        timeTagfile = curfol + '_Timetag.txt'
        errorfile = curfol + '_Errorlist.txt'
        if os.path.exists(timeTagfile):
            os.remove(timeTagfile)
        if os.path.exists(errorfile):
            os.remove(errorfile)
        timeTagTxt = open(timeTagfile, 'a+')
        errorTxt = open(errorfile, 'a+')
        time = []
        reader = open(logfile, 'r')
        line = reader.readline()
        timeTagTxt.write('\n' + '=' * 20 + ' Time Tag Start ' + '=' * 20 + '\n')
        while not line == '':
            if "bash arg:" in line:
                timeTagTxt.write(line)
            if "system_uptime:" in line:
                timeTagTxt.write(line)
                time.append(line.strip().split(' ')[3].split(':')[1].strip(']'))
            # print(line)
            if "CRASH:" in line:
                errorTxt.write(line)
                timeTagTxt.write(line)
            if "NOT RESPONDING:" in line:
                errorTxt.write(line)
                timeTagTxt.write(line)
            if "// Short Msg: Native crash" in line:
                errorTxt.write(line)
            if "No activities found to run, monkey aborted" in line:
                errorTxt.write(line)
                timeTagTxt.write(line)
            if "Monkey finished" in line:
                timeTagTxt.write(line)
            if "Network stats" in line:
                timeTagTxt.write(line)
            line = reader.readline()
        # calc monkey running time
        start = 0
        end = 0
        try:
            start = long(time[0])
            end = long(time[-1])
        except  Exception:
            print "Error:Monkey is abnormal No time Tag Founded...."
        print("start =" + str(start))
        print("end =" + str(end))
        runtime = timeShift(end - start)
        timeTagTxt.writelines('\n' + '\n' + '=' * 20 + ' Test Result ' + '=' * 20 + '\n')
        timeTagTxt.writelines("StartTimeTag: %s\nEndTimeTag: %s\n" % (start, end))
        timeTagTxt.writelines("TotalRuntime: %d hor %d min %d sec\n" % (runtime[0], runtime[1], runtime[2]))
        timeTagTxt.write('Monkey Running time >6h :' + str(runtime[0] >= 6))
        timeTagTxt.close()
        errorTxt.close()
        has_error = get_error_time(errorfile)
        all_log_path = os.path.dirname(errorfile.replace("MonkeyLog","AllLog"))
        phone_tag=logfile.split('#')[0].split(os.sep)[-1]+'#'
        ret.append(phone_tag)
        ret.append(start)
        ret.append(end)
        ret.append(runtime)
        if not has_error:
            del_unusful_log(all_log_path)
            pass
        print("Analyse Result Finished...")
    else:
        print("Monkey log file isn`t exists.")
    return ret



def getInfoDuring():
    print('Analysing Results While during Test...')
    resultfolder = os.getcwd() + os.sep + 'MonkeyLog'
    models = os.listdir(resultfolder)
    for model in models:
        modelfolder = os.path.join(resultfolder, model)
        devices = os.listdir(modelfolder)
        for device in devices:
            device_folder = os.path.join(modelfolder, device)
            logs = os.listdir(device_folder)
            for log in logs:
                if log.strip('.txt')[-2::].isdigit():
                    log_path = os.path.join(device_folder, log)
                    print "file_path = " + log_path
                    getusefulInfo(log_path)


def get_error_time(filepath):
    flag = False
    path = os.path.dirname(filepath)
    filebasename = os.path.basename(filepath).strip("Errorlist.txt")
    error_count = path + os.sep + filebasename + "Errorcount.txt"
    if os.path.exists(error_count):
        os.remove(error_count)
    else:
        pass
    errorCount = open(error_count, 'a+')
    reader = open(filepath, 'r')
    # errorname：times
    tmp = {}
    for num, value in enumerate(reader):
        str_error = re.sub(u"\\(.*?\\)", "", value.strip().strip("// ")).strip()
        if "Short Msg: Native crash" in value:
            be = linecache.getline(filepath, num)
            str_error = re.sub(u"\\(.*?\\)", "", be.strip().strip("// ")).strip()
            tmp[str_error] = int(tmp[str_error]) - 1
            str_error = "[tombstones] " + str_error
            # continue
        if str_error in tmp.keys():
            tmp[str_error] = tmp[str_error] + 1
        else:
            tmp[str_error] = 1

    # print tmp
    for key in tmp.keys():
        if not tmp[key] == 0:
            errorCount.writelines(key + '=' + str(tmp[key]) + '\n')
            flag = True
    errorCount.close()
    return flag


def del_unusful_log(path):
    print path
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)


if __name__ == '__main__':
    # log_file = '/home/wangzhen/monkeyAutoTest/MonkeyLog/com.android.contacts/L0317#/com.android.contacts_900333_14_01_54.txt'
    # getusefulInfo(log_file)
    getInfoDuring()
