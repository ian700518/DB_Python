#!/usr/bin/python

import logging
import subprocess
import json
import time
import os
from subprocess import PIPE

logger_sub = logging.getLogger('SUBP_LOG')


class ChargeDevice :
    def __init__(self, idx = 0, type = '', mac = '', account = '', uid = '', STime = 0, CTime = 0,
                    FSTime = '', FCTime = '', CM = 0, RT_H = 0, RT_M = 0) :
        self.Dev_idx = idx
        self.Dev_type = type
        self.Dev_mac = mac
        self.Dev_account = account
        self.Dev_uid = uid
        self.StartTime = STime
        self.CurrentTime = CTime
        self.DevFormatSTime = FSTime
        self.DevFormatCTime = FCTime
        self.ChgMode = CM
        self.RemainT_Hr = RT_H
        self.RemainT_Min = RT_M
    def getidx(self) :
        return self.Dev_idx
    def gettype(self) :
        return self.Dev_type
    def getmac(self) :
        return self.Dev_mac
    def getaccount(self) :
        return self.Dev_account
    def getuid(self) :
        return self.Dev_uid
    def getstime(self) :
        return self.StartTime
    def getctime(self) :
        return self.CurrentTime
    def getfstime(self) :
        return self.DevFormatSTime
    def getfctime(self) :
        return self.DevFormatCTime
    def getmode(self) :
        return self.ChgMode
    def getrth(self) :
        return self.RemainT_Hr
    def getrtm(self) :
        return self.RemainT_Min

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
    list = []
    for i in range(0, CDCt) :
        list.append(CDV[i].__dict__)
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
        if CDV[i].getuid() == dict_text['userId'] :
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

def GetDeviceMACAddr(path) :
    logger_sub.info('into Get Device Network Macaddress~~!!')
    with open('/etc/config/network', 'r') as fp :
        while 1 :
            str_net = fp.readline()
            if str_net != '' :
                if str_net.find('macaddr') != -1 :
                    str1_net = str_net[-19 : -2]    # ''' get macaddress xx:xx:xx:xx:xx:xx '''
                    logger_sub.debug('str1_net : {},str_net : {}'.format(str1_net, str_net))
                    break
            else :
                break
    with open(path, 'r+') as fp :
        s= fp.read(512)
        logger_sub.debug('GetDeviceMACAddr File is {}'.format(s))
        dict_text = json.loads(s)
        logger_sub.debug('json to python is {}'.format(dict_text))
        dict_text['Network MAC Address'] = '{}'.format(str1_net)
        text_json = json.dumps(dict_text, sort_keys = True, indent = 4, separators = (',',':'))
        logger_sub.debug('python to json is {}'.format(text_json))
        fp.seek(os.SEEK_SET)
        fp.write(text_json)
