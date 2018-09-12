#!/usr/bin/python

import logging
import subprocess
import json
import time
from subprocess import PIPE

logger_sub = logging.getLogger('SUBP_LOG')

class ChargeDevice :
    def __init__(self, Dev_idx = 0, Dev_type = '', Dev_mac = '', Dev_account = '', Dev_uid = '', StartTime = 0, CurrentTime = 0,
                    DevFormatSTime = '', DevFormatCTime = '', ChgMode = 0, RemainT_Hr = 0, RemainT_Min = 0) :
        self.Dev_idx = Dev_idx
        self.Dev_type = Dev_type
        self.Dev_mac = Dev_mac
        self.Dev_account = Dev_account
        self.Dev_uid = Dev_uid
        self.StartTime = StartTime
        self.CurrentTime = CurrentTime
        self.DevFormatSTime = DevFormatSTime
        self.DevFormatCTime = DevFormatCTime
        self.ChgMode = ChgMode
        self.RemainT_Hr = RemainT_Hr
        self.RemainT_Min = RemainT_Min

def Send_Command(command) :
    p = subprocess.Popen(command, shell = True, stdout = PIPE)
    #s = p.communicate()
    s = p.stdout.read()
    logger_sub.debug('Command reply is {}'.format(s))
    return s

def AddSymbolForMac(str) :
    logger_sub.info('into Add Symbol For iOS Mac information~~!!')
    Rstr = []
    for index, char in enumerate(str) :
        Rstr.append(char)
        if index % 2 == 1 and index != 11:
            Rstr.append(':')
    return Rstr

def GetChgDevFromFile(path, CDV) :
    logger_sub.info('into Get Charge Device From File function~~!!')
    try :
        fp = open('/DaBai/python/OnlineChgList.json', 'r')
        json_s = fp.read()
        list_f = json.loads(json_s)
        List_len = len(list_f)
        logger_sub.debug('List_len is {}'.format(List_len))
        for i in range(0, List_len) :
            dict = list_f[i]
            CDV.append(ChargeDevice(dict['Dev_idx'], dict['Dev_type'], dict['Dev_mac'], dict['Dev_account'], dict['Dev_uid'],
                                        dict['StartTime'], dict['CurrentTime'], dict['DevFormatSTime'], dict['DevFormatCTime'],
                                        dict['ChgMode'], dict['RemainT_Hr'], dict['RemainT_Hr']))
            logger_sub.debug('idx : {},\ntype : {},\nmac : {},\naccount : {},\nuid : {}\n'.format(CDV[i].Dev_idx, CDV[i].Dev_type, CDV[i].Dev_mac, CDV[i].Dev_account, CDV[i].Dev_uid))
        fp.close()
    except IOError :
        CDV = [ChargeDevice()]
        List_len = 0
        logger_sub.error('OnlineChgList.json can not find~~!!')
    return List_len

def WriteChageList(path, CDV, CDCt) :
    logger_sub.info('Into Write Charge List function ~~!!')
    dict = {'Dev_idx':0, 'Dev_type':'', 'Dev_mac':'', 'Dev_account':'', 'Dev_uid':'', 'StartTime':0, 'CurrentTime':0,
            'DevFormatSTime':'', 'DevFormatCTime':'', 'ChgMode':0, 'RemainT_Hr':0, 'RemainT_Min':0}
    list = []
    for i in range(0, CDCt) :
        dict['Dev_idx'] = CDV[i].Dev_idx
        dict['Dev_type'] = CDV[i].Dev_type
        dict['Dev_mac'] = CDV[i].Dev_mac
        dict['Dev_account'] = CDV[i].Dev_account
        dict['Dev_uid'] = CDV[i].Dev_uid
        dict['StartTime'] = CDV[i].StartTime
        dict['CurrentTime'] = CDV[i].CurrentTime
        dict['DevFormatSTime'] = CDV[i].DevFormatSTime
        dict['DevFormatCTime'] = CDV[i].DevFormatCTime
        dict['ChgMode'] = CDV[i].ChgMode
        dict['RemainT_Hr'] = CDV[i].RemainT_Hr
        dict['RemainT_Min'] = CDV[i].RemainT_Min
        list.append(dict)
    logger_sub.debug('dict is {}'.format(list))
    json_s = json.dumps(list, sort_keys = True, indent = 2, separators = (',',':'))
    logger_sub.debug('json_s is {}'.format(json_s))
    with open(path, 'w+') as fp :
        fp.write(json_s)

def CheckCHGDevInfo(path, CDV, CDCt) :
    logger_sub.info('into Check Charge Device Information (List)~~!!')
    i = 0
    with open(path, 'r') as fp :
        s = fp.read(512)
        dict_text = json.loads(s)
    cur_time = time.time()
    for i in range(0, CDCt) :
        if CDV[i].Dev_uid == dict_text['userId'] :
            break
    if i == CDCt :
        logger_sub.warning('Get a new charge device ~~~!!!')
        CDV[i].Dev_idx = CDCt
        CDV[i].Dev_type = dict_text['type']
        if CDV[i].Dev_type == 'iOS' :
            mactmp = dict_text['mac'].split('-')
            mactmp1 = AddSymbolForMac(mactmp[4])
            CDV[i].Dev_mac = '{}'.format(''.join(mactmp1))
        else :
            CDV[i].Dev_mac = dict_text['mac']
        CDV[i].Dev_account = dict_text['account']
        CDV[i].Dev_uid = dict_text['userId']
        CDV[i].StartTime = cur_time
        CDV[i].CurrentTime = cur_time
        CDV[i].DevFormatSTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_time))
        CDV[i].DevFormatCTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_time))
        logger_sub.debug('idx : {},\ntype : {},\nmac : {},\naccount : {},\nuid : {}\n'.format(CDV[CDCt].Dev_idx, CDV[CDCt].Dev_type, CDV[CDCt].Dev_mac, CDV[CDCt].Dev_account, CDV[CDCt].Dev_uid))
        if CDCt < 4 :
            CDCt += 1
    else :
        logger_sub.warning('charge device already at charge list ~~~!!!')
        CDV[i].CurrentTime = cur_time
        CDV[i].DevFormatCTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_time))
    WriteChageList('/DaBai/python/OnlineChgList.json', CDV, CDCt)
    return CDCt
