#!/usr/bin/python

import serial
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

serial_path = '/dev/ttyS2'
serial_baud = 57600
serial_parity = 'N'
serial_bits = 8
serial_stop = 1
serial_timeout = 0.01

GPIO_USB1PWR_NUM = 4
GPIO_USB2PWR_NUM = 5
GPIO_WCEN_NUM = 18
GPIO_WCRDY_NUM = 19
GPIO_SWBTN_NUM = 0
GPIO_WAKEUP_NUM = 2
GPIO_RESET_NUM = 3
GPIO_P04_NUM = 45
GPIO_P15_NUM = 1
GPIO_P20_NUM = 46
GPIO_P24_NUM = 6
GPIO_EAN_NUM = 11

DIRECT_OUT = 1
DIRECT_IN = 0

print 'mt7688_pinmux set i2c gpio receive = ', Send_Command('mt7688_pinmux set i2c gpio')
print 'mt7688_pinmux set uart1 gpio receive = ', Send_Command('mt7688_pinmux set uart1 gpio')
print 'mt7688_pinmux set pwm0 gpio receive = ', Send_Command('mt7688_pinmux set pwm0 gpio')
print 'mt7688_pinmux set pwm1 gpio receive = ', Send_Command('mt7688_pinmux set pwm1 gpio')

if GpioInitial(GPIO_USB1PWR_NUM, DIRECT_OUT, 1) != 1 :
    print 'GPIO_USB1PWR_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_USB2PWR_NUM, DIRECT_OUT, 1) != 1 :
    print 'GPIO_USB2PWR_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_WCEN_NUM, DIRECT_OUT, 1) != 1 :
    print 'GPIO_WCEN_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_WCRDY_NUM, DIRECT_IN, 0) != 1 :
    print 'GPIO_WCRDY_NUM Initialization faild~~~!!!'

if GpioInitial(GPIO_SWBTN_NUM, DIRECT_OUT, 0) != 1 :
    print 'GPIO_SWBTN_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_WAKEUP_NUM, DIRECT_OUT, 0) != 1 :
    print 'GPIO_WAKEUP_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_RESET_NUM, DIRECT_OUT, 0) != 1 :
    print 'GPIO_RESET_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_P20_NUM, DIRECT_OUT, 0) != 1 :
    print 'GPIO_P20_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_P24_NUM, DIRECT_OUT, 0) != 1 :
    print 'GPIO_P24_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_EAN_NUM, DIRECT_OUT, 0) != 1 :
    print 'GPIO_EAN_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_P04_NUM, DIRECT_IN, 0) != 1 :
    print 'GPIO_P04_NUM Initialization faild~~~!!!'
if GpioInitial(GPIO_P15_NUM, DIRECT_IN, 0) != 1 :
    print 'GPIO_P15_NUM Initialization faild~~~!!!'

rxbuf = []
filebuf = []
SetBMModuleMode(0)
#BTTransferUart('/DaBai/python/RxCommTmp.txt', rxbuf, filebuf)
#ChangBTName('/DaBai/python/RxCommTmp.txt', rxbuf, filebuf)
#GetBTModuleName('/DaBai/python/HostDeviceInfo.json', rxbuf)
#GetBTModuleInof('/DaBai/python/HostDeviceInfo.json', rxbuf, filebuf)
#Dserial = OpenSerial(serial_path, serial_baud, serial_bits, serial_parity, serial_stop, serial_timeout)
