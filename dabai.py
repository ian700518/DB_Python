#!/usr/bin/python

import logging
import serial
import json
from subproc import Send_Command
from Dgpio import SetGpio
from Dgpio import GetGpio
from Dgpio import GpioInitial
from bt import SetBMModuleMode
from bt import GetBTModuleInof
from bt import GetBTModuleName
from bt import SetBTModuleName
from bt import ChangBTName
from bt import BTTransferUart
from Duart import OpenSerial
from Duart import UartPara
from subproc import ChargeDevice
from subproc import CheckCHGDevInfo
from subproc import GetChgDevFromFile
from subproc import GetDeviceMACAddr
from Dgpio import GPIO_SWBTN_NUM
from Dgpio import GPIO_WAKEUP_NUM
from Dgpio import GPIO_RESET_NUM
from Dgpio import GPIO_P04_NUM
from Dgpio import GPIO_P15_NUM
from Dgpio import GPIO_P20_NUM
from Dgpio import GPIO_P24_NUM
from Dgpio import GPIO_EAN_NUM
from Dgpio import GPIO_USB1PWR_NUM
from Dgpio import GPIO_USB2PWR_NUM
from Dgpio import GPIO_WCEN_NUM
from Dgpio import GPIO_WCRDY_NUM
from Dgpio import DIRECT_OUT
from Dgpio import DIRECT_IN
from bt import RXBUFSIZE

# basic configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/DaBai/python/system.log',
                    filemode='w+')
# define handler output to sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# setting output protocol
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# handler setting output protocol
console.setFormatter(formatter)
# add hander into root logger
logging.getLogger('').addHandler(console)
#logger_DABAI = logging.getLogger('Dabai_LOG')

Send_Command('mt7688_pinmux set i2c gpio')
Send_Command('mt7688_pinmux set uart1 gpio')
Send_Command('mt7688_pinmux set pwm0 gpio')
Send_Command('mt7688_pinmux set pwm1 gpio')

if GpioInitial(GPIO_USB1PWR_NUM, DIRECT_OUT, 1) != 1 :
    logging.error('GPIO_USB1PWR_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_USB2PWR_NUM, DIRECT_OUT, 1) != 1 :
    logging.error('GPIO_USB2PWR_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_WCEN_NUM, DIRECT_OUT, 1) != 1 :
    logging.error('GPIO_WCEN_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_WCRDY_NUM, DIRECT_IN, 0) != 1 :
    logging.error('GPIO_WCRDY_NUM Initialization faild~~~!!!')

if GpioInitial(GPIO_SWBTN_NUM, DIRECT_OUT, 0) != 1 :
    logging.error('GPIO_SWBTN_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_WAKEUP_NUM, DIRECT_OUT, 0) != 1 :
    logging.error('GPIO_WAKEUP_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_RESET_NUM, DIRECT_OUT, 0) != 1 :
    logging.error('GPIO_RESET_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_P20_NUM, DIRECT_OUT, 0) != 1 :
    logging.error('GPIO_P20_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_P24_NUM, DIRECT_OUT, 0) != 1 :
    logging.error('GPIO_P24_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_EAN_NUM, DIRECT_OUT, 0) != 1 :
    logging.error('GPIO_EAN_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_P04_NUM, DIRECT_IN, 0) != 1 :
    logging.error('GPIO_P04_NUM Initialization faild~~~!!!')
if GpioInitial(GPIO_P15_NUM, DIRECT_IN, 0) != 1 :
    logging.error('GPIO_P15_NUM Initialization faild~~~!!!')

rxbuf = []
filebuf = []
ChgDev = []
command_idx = 0
ChgDevCt = 0
SetBMModuleMode(0)
Dser_para = UartPara()
Dser = OpenSerial(Dser_para)
while 1 :
    rxbuf = Dser.read(RXBUFSIZE)
    if len(rxbuf) > 0 :
        if (rxbuf[0] == 0xAA) and (rxbuf[3] == 0x8F) and (rxbuf[4] == 0x01) :
            rxbuf = []
            break
Dser.close()
GetBTModuleInof('/DaBai/python/HostDeviceInfo.json', rxbuf)
GetBTModuleName('/DaBai/python/HostDeviceInfo.json', rxbuf)
BTModuleLeaveConfigMode(rxbuf)
GetDeviceMACAddr('/DaBai/python/HostDeviceInfo.json')

ChgDevCt = GetChgDevFromFile('/DaBai/python/OnlineChgList.json', ChgDev)

while 1 :
    command_idx = BTTransferUart('/DaBai/python/RxCommTmp.txt', rxbuf, filebuf)
    if command_idx == 1 :
        logging.debug('command_idx is 1 ~~!!')
    elif command_idx == 2 :
        logging.debug('command_idx is 2 ~~!!')
        ChgDevCt = CheckCHGDevInfo('/DaBai/python/RxCommTmp.txt', ChgDev, ChgDevCt)
    elif command_idx == 3 :
        logging.debug('command_idx is 3 ~~!!')


#ChangBTName('/DaBai/python/RxCommTmp.txt', rxbuf, filebuf)
#GetBTModuleName('/DaBai/python/HostDeviceInfo.json', rxbuf)
#GetBTModuleInof('/DaBai/python/HostDeviceInfo.json', rxbuf, filebuf)
#Dserial = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
