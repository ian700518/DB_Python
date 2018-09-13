#!/usr/bin/python

import logging
import serial
import json
from Dgpio import SetGpio, GetGpio, GpioInitial, PinInitial
from bt import SetBMModuleMode, GetBTModuleInof, GetBTModuleName, BTTransferUart, RXBUFSIZE
from subproc import ChargeDevice, CheckCHGDevInfo, GetChgDevFromFile, GetDeviceMACAddr, Send_Command
from Duart import OpenSerial, UartPara

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

rxbuf = []
filebuf = []
ChgDev = []
command_idx = 0
ChgDevCt = 0

Send_Command('mt7688_pinmux set i2c gpio')
Send_Command('mt7688_pinmux set uart1 gpio')
Send_Command('mt7688_pinmux set pwm0 gpio')
Send_Command('mt7688_pinmux set pwm1 gpio')

PinInitial()
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
