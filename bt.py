#!/usr/bin/python

import os
import json
import time
import serial
from subproc import Send_Command
from Dgpio import SetGpio
from Duart import OpenSerial

serial_path = '/dev/ttyS2'
serial_baud = 57600
serial_parity = 'N'
serial_bits = 8
serial_stop = 1
serial_timeout = 0.01

BM78SPP05MC2 = 1
BM78SPP05NC2 = 0

GPIO_SWBTN_NUM = 0
GPIO_WAKEUP_NUM = 2
GPIO_RESET_NUM = 3
GPIO_P04_NUM = 45
GPIO_P15_NUM = 1
GPIO_P20_NUM = 46
GPIO_P24_NUM = 6
GPIO_EAN_NUM = 11

RXBUFSIZE = 256
FILESIZE = 4096

def SetBMModuleMode(OPmode) :
    time.sleep(0.001)
    SetGpio(GPIO_WAKEUP_NUM, 1)
    if OPmode == 1 :
        if BM78SPP05MC2 == 1 :
            SetGpio(GPIO_EAN_NUM, 0)
        else :
            SetGpio(GPIO_EAN_NUM, 1)
        SetGpio(GPIO_P20_NUM, 0)
        SetGpio(GPIO_P24_NUM, 1)
    else :
        if BM78SPP05MC2 == 1 :
            SetGpio(GPIO_EAN_NUM, 0)
        else :
            SetGpio(GPIO_EAN_NUM, 1)
        SetGpio(GPIO_P20_NUM, 0)
        SetGpio(GPIO_P24_NUM, 1)
    SetGpio(GPIO_SWBTN_NUM, 1)
    time.sleep(0.04)
    SetGpio(GPIO_RESET_NUM, 1)
    time.sleep(0.45)

def CheckBTCommandCheckSum(Buf) :
    Cst = 0
    i = 0
    len = Buf[2] + 2
    while (i < len) :
        Cst -= Buf[i+1]
        i = i + 1
    return (Cst & 0x00FF)

def GetBTModuleInof(path, rxbuf, filebuf) :
    rxbuf = []
    filebuf = []
    macaddr = []
    Dser = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
    BTBuf = [0xAA, 0x00, 0x01, 0x01]
    BTBuf.append(CheckBTCommandCheckSum(BTBuf))
    print 'BTBuf[{}]'.format(','.join(hex(x) for x in BTBuf))
    Sendct = Dser.write(BTBuf)
    time.sleep(0.01)
    rxbuf = Dser.read(RXBUFSIZE)
    #rxbuf = [0xaa, 0x00, 0x0e, 0x80, 0x01, 0x00, 0x22, 0x20, 0x00, 0x01, 0x03, 0xeb, 0x22, 0xf4, 0x81, 0x34, 0x62]
    if len(rxbuf) > 0 :
        print 'GetBTModuleInfo rxbuf[{}]'.format(','.join(hex(x) for x in rxbuf))
        with open(path, 'r+') as fp :
            s = fp.read(512)
            print 'File is {}'.format(s)
            dict_text = json.loads(s)
            print 'json to python is {}'.format(dict_text)
            macaddr.append('{:2x}'.format(rxbuf[9] << 4 | rxbuf[10]))
            macaddr.append('{:2x}'.format(rxbuf[11]))
            macaddr.append('{:2x}'.format(rxbuf[12]))
            macaddr.append('{:2x}'.format(rxbuf[13]))
            macaddr.append('{:2x}'.format(rxbuf[14]))
            macaddr.append('{:2x}'.format(rxbuf[15]))
            print 'macaddr is {}'.format(macaddr)
            macstr = ':'.join(macaddr)
            dict_text['Bluetooth MAC Address'] = '{}'.format(macstr)
            text_json = json.dumps(dict_text, sort_keys = True, indent = 4, separators=(',',':'))
            print 'python to json is {}'.format(text_json)
            fp.seek(os.SEEK_SET);
            fp.write(text_json)
            fp.close()
    Dser.close()

def GetBTModuleName(path, rxbuf) :
    rxbuf = []
    Dser = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
    BTBuf = [0xAA, 0x00, 0x01, 0x07]
    BTBuf.append(CheckBTCommandCheckSum(BTBuf))
    print 'BTBuf[{}]'.format(','.join(hex(x) for x in BTBuf))
    while 1 :
        namebuf = []
        Sendct = Dser.write(BTBuf)
        time.sleep(0.01)
        rxbuf = Dser.read(RXBUFSIZE)
        #rxbuf = [0xaa, 0x00, 0x12, 0x80, 0x07, 0x00, 0x44, 0x42, 0x5F, 0x30, 0x30, 0x31, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x30, 0x33, 0x3c]
        rxlength = len(rxbuf)
        print 'rxlength is {}'.format(rxlength)
        for i in range(0, rxlength - 7) :
            namebuf.append(rxbuf[i + 6])
        print 'namebuf is {}'.format(namebuf)
        if rxlength > 0 :
            checksum = CheckBTCommandCheckSum(rxbuf)
            if checksum != rxbuf[rxlength - 1] :
                continue
            btname = '{}'.format(''.join(chr(x) for x in namebuf))
            print 'btname is {}'.format(btname)
            with open(path, 'r+') as fp :
                s= fp.read(512)
                print 'File is {}'.format(s)
                dict_text = json.loads(s)
                print 'json to python is {}'.format(dict_text)
                dict_text['Bluetooth Device Name'] = '{}'.format(btname)
                text_json = json.dumps(dict_text, sort_keys = True, indent = 4, separators = (',',':'))
                print 'python to json is {}'.format(text_json)
                fp.seek(os.SEEK_SET)
                fp.write(text_json)
                fp.close()
        Dser.close()
        break

def SetBTModuleName(rxubf, btname) :
    rxbuf = []
    BTMName = []
    Dser = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
    lenbtname = len(btname) + 2
    print 'lenbtname is {:d}'.format(lenbtname)
    BTMName.append(0xAA)
    BTMName.append(lenbtname >> 8)
    BTMName.append(lenbtname & 0xFF)
    BTMName.append(0x08)
    BTMName.append(0x01)
    for i in btname :
        BTMName.append(ord(i))
    BTMName.append(CheckBTCommandCheckSum(BTMName))
    print 'BTMName is {}'.format(BTMName)
    while 1 :
        Sendct = Dser.write(BTMName)
        time.sleep(0.01)
        rxbuf = Dser.read(RXBUFSIZE)
        rxlength = len(rxbuf)
        if rxlength > 0 :
            checksum = CheckBTCommandCheckSum(rxbuf)
            if checksum != rxbuf[rxlength - 1] :
                continue
            if(rxbuf[0] == 0xAA) and (rxbuf[3] == 0x80) and (rxbuf[4] == 0x08) :
                time.sleep(0.5)
                SetGpio(GPIO_RESET_NUM, 0)
                time.sleep(0.001)
                SetGpio(GPIO_RESET_NUM, 1)
                rxbuf = []
                while 1 :
                    rxbuf = Dser.read(RXBUFSIZE)
                    rxlength = len(rxbuf)
                    if rxlength > 0 :
                        if(rxbuf[0] == 0xAA) and (rxbuf[3] == 0x8F) and (rxbuf[4] == 0x01) :
                            break
                Dser.close()
                break


def BTModuleLeaveConfigMode(rxbuf) :
    rxbuf = []
    Dser = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
    BTBuf = [0xAA, 0x00, 0x02, 0x52, 0x00]
    BTBuf.append(CheckBTCommandCheckSum(BTBuf))
    print 'BTBuf[{}]'.format(','.join(hex(x) for x in BTBuf))
    while 1 :
        Sendct = Dser.write(BTBuf)
        time.sleep(0.01)
        rxbuf = Dser.read(RXBUFSIZE)
        rxlength = len(rxbuf)
        if rxlength > 0 :
            checksum = CheckBTCommandCheckSum(rxbuf)
            if checksum != rxbuf[rxlength - 1] :
                continue
            if rxbuf[0] == 0xAA and rxbuf[3] == 0x8F and rxbuf[4] == 0x00 :
                print 'BT Module Leave Config Mode !!!'
        Dser.close()
        break

def ChangBTName(path, rxbuf, filebuf) :
    rxbuf = []
    filebuf = []
    LocalBTMac = []
    CommBTMac = []
    NewBTName = []

    with open('/DaBai/python/HostDeviceInfo.json', 'r+') as fp :
        s = fp.read(512)
        dict_text = json.loads(s)
        LocalBTMac = dict_text['Bluetooth MAC Address']
        print 'LocalBTMac is {}'.format(LocalBTMac)
        fp.close()

    with open(path, 'r+') as fp :
        s = fp.read(512)
        dict_text = json.loads(s)
        CommBTMac = dict_text['BTMac']
        NewBTName = dict_text['BTName']
        print 'BTMac is {}, BTName is {}'.format(CommBTMac, NewBTName)
        fp.close()

    if LocalBTMac == CommBTMac :
        print 'LocalBTMac equal to CommBTMac'
        Dser = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
        rxbuf = '{} Receive ChangBTName Command~~!!'.format(LocalBTMac)
        Sendct = Dser.write(rxbuf)
        time.sleep(0.01)
        SetGpio(GPIO_RESET_NUM, 0)
        time.sleep(0.001)
        SetGpio(GPIO_RESET_NUM, 1)
        rxbuf = []
        while 1 :
            rxbuf = Dser.read(512)
            rxlength = len(rxbuf)
            if rxlength > 0 :
                if(rxbuf[0] == 0xAA) and (rxbuf[3] == 0x8F) and (rxbuf[4] == 0x01) :
                    rxbuf = []
                    break
        Dsr.close()
        BTModuleChgDevName(rxbuf, NewBTName);
        GetBTModuleName('/DaBai/python/HostDeviceInfo.json', rxbuf, filebuf);
        BTModuleLeaveConfigMode(rxbuf);

def BTTransferUart(path, rxbuf, filebuf) :
    rxbuf = []
    filebuf = []
    IOSSUFFIX = 'AAEnd'
    Dser = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
    rxbuf = Dser.read(RXBUFSIZE)
    #with open('/DaBai/python/RxCommTmp.txt', 'r') as fp :
    #    rxbuf = fp.read(RXBUFSIZE)
    #    fp.close()
    rxlength = len(rxbuf)
    if rxlength > 0 :
        print 'rxbuf is {}, length is {}'.format(rxbuf, rxlength)
        if is_json(rxbuf) == True :
            dict_text = json.loads(rxbuf)
            idx = int(dict_text['index'], 10)
            dev_type = dict_text['type']
            print 'idx is {}, dev_type is {}'.format(idx, dev_type)
            if idx > 0 :
                with open(path, 'w+') as fp :
                    fp.write(rxbuf)
                    fp.close()
                if idx == 2 :
                    with open('/DaBai/python/chongdian.jpeg', 'r') as fp :
                        Sendct = 0
                        while 1 :
                            filebuf = fp.read(FILESIZE)
                            if filebuf != '' :
                                Sendct += Dser.write(filebuf)
                                print 'Send total count is {}'.format(Sendct)
                            else :
                                break

                        if dev_type == 'iOS' :
                            Sendct = Dser.write(IOSSUFFIX)
                        fp.close()
        else :
            print 'RX Command is not JSON protocol'
            with open('/DaBai/python/ErrorCmd.txt', 'w+') as fp :
                fp.write(rxbuf)
                fp.close()
    Dser.close()

def is_json(json_str) :
    try:
        json_object = json.loads(json_str)
    except ValueError, e:
        return False
    return True
