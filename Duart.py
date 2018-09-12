#!/usr/bin/python

import logging
import serial

logger_uart = logging.getLogger('UART_LOG')

def OpenSerial(dev, serbaud, serbit, serparity, serstop, sertimeout) :
    logger_uart.info('into Serial Open function')
    logger_uart.warning('dev : {:s},\n Baudrate : {:d},\n Datalength : {:d},\n Parity : {:s},\n Stopbit : {:d},\n Timeout : {:f}ms\n'.format(dev, serbaud, serbit, serparity, serstop, (sertimeout * 1000)))
    if serparity == 'O' or serparity == 'o' :
        sparity = serial.PARITY_ODD
    elif serparity == 'E' or serparity == 'e' :
        sparity = serial.PARITY_EVEN
    else :
        sparity = serial.PARITY_NONE

    if serstop == 1 :
        sstop = serial.STOPBITS_ONE
    elif serstop == 1.5 :
        sstop = serial.STOPBITS_ONE_POINT_FIVE
    else :
        sstop = serial.STOPBITS_TWO

    if serbit == 5 :
        sbit = serial.FIVEBITS
    elif serbit == 6 :
        sbit = serial.SIXBITS
    elif serbit == 7 :
        sbit = serial.SEVENBITS
    else :
        sbit = serial.EIGHTBITS

    if serbaud < 9600 :
        sbaud = 9600
    elif serbaud > 115200 :
        sbaud = 115200
    else :
        sbaud = serbaud
    return serial.Serial(dev, baudrate = sbaud, bytesize = sbit, parity = sparity, stopbits = sstop, timeout = sertimeout)
