#!/usr/bin/python3

import logging
import serial
import json
import select
import threading
import time
import sys
from Dgpio import SetGpio, GetGpio, GpioInitial, PinInitial
from bt import SetBMModuleMode, GetBTModuleInof, GetBTModuleName, BTModuleLeaveConfigMode, BTTransferUart, RXBUFSIZE
from subproc import ChargeDevice, CheckCHGDevInfo, GetChgDevFromFile, GetDeviceMACAddr, Send_Command
from Duart import OpenSerial, UartPara
from hsocket import dbthread

"""
* logging.debug()
* logging.info()
* logging.warning()
* logging.error()
* logging.critical()
class sorting
NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
"""
# basic configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/DaBai/python/system.log',
                    filemode='w+')
# define handler output to sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
# setting output protocol
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# handler setting output protocol
console.setFormatter(formatter)
# add hander into root logger
logging.getLogger('').addHandler(console)
#logger_DABAI = logging.getLogger('Dabai_LOG')

def main(argv) :
    rxbuf = []
    filebuf = []
    ChgDev = []
    command_idx = 0
    ChgDevCt = 0

    logging.debug('argv is {}'.format(argv))

    Send_Command('mt7688_pinmux set i2c gpio')
    Send_Command('mt7688_pinmux set uart1 gpio')
    Send_Command('mt7688_pinmux set pwm0 gpio')
    Send_Command('mt7688_pinmux set pwm1 gpio')

    #comm = 'devmem 0x1000003C'
    #original_val = int(Send_Command(comm), 16)
    #original_val |= 0x000E000F
    #comm = 'devmem 0x1000003C 32 0x{:08x}'.format(original_val)
    #Send_Command(comm)

    #Send_Command('devmem 0x10000e24 32 0x00000001')        """ Set Uart2 HighSpeed to 1, and real uart2 baudrate will used 115200 """

    #Dser_para = UartPara()
    #Dser = OpenSerial(Dser_para)
    #PinInitial()
    #SetBMModuleMode(0)
    #while 1 :
    #    Dser_readable,Dser_writable,Dser_exceptional = select.select([Dser], [], [], 0.03)
    #    if Dser_readable :
    #        rxbuf.append(ord(Dser.read()))
    #    else :
    #        if len(rxbuf) > 0 :
    #            logging.warning('rxbuf is {}'.format(rxbuf))
    #            if (rxbuf[0] == 0xAA) and (rxbuf[3] == 0x8F) and (rxbuf[4] == 0x01) :
    #                rxbuf = []
    #                break
    #            rxbuf = []
    #
    #Dser.close()
    #GetBTModuleInof('/DaBai/python/HostDeviceInfo.json', rxbuf)
    #GetBTModuleName('/DaBai/python/HostDeviceInfo.json', rxbuf)
    #BTModuleLeaveConfigMode(rxbuf)
    #GetDeviceMACAddr('/DaBai/python/HostDeviceInfo.json')

    ChgDevCt = GetChgDevFromFile('/DaBai/python/OnlineChgList.json', ChgDev)

    """ Create Pthread """
    try:
        thread1 = dbthread(1, 'Thread-1', '192.168.100.107', 12345)
        thread1.start()
    except:
        logging.error('Thread Create error~~!!')

    while 1 :
        command_idx = BTTransferUart('/DaBai/python/RxCommTmp.txt', rxbuf, filebuf)
        if command_idx == 1 :   # Set Device Network Information
            logging.debug('command_idx is 1 ~~!!')
        elif command_idx == 2 :   # Devive Send Account and Devive information to check will be charged
            logging.debug('command_idx is 2 ~~!!')
            ChgDevCt = CheckCHGDevInfo('/DaBai/python/RxCommTmp.txt', ChgDev, ChgDevCt)
        elif command_idx == 3 :   # Set Bluetooth Device Name
            ChangBTName('/DaBai/python/RxCommTmp.txt', rxbuf, filebuf)
            logging.debug('command_idx is 3 ~~!!')

if __name__ == "__main__":
   main(sys.argv)
