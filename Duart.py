#!/usr/bin/python

import logging
import serial

logger_uart = logging.getLogger('UART_LOG')

class UartPara :
    def __init__(self, port = '/dev/ttyS2', br = 57600, db = 8, pr = 'N', sb = 1, to = 0.01) :
        self.devpath = port
        self.baudrate = br
        self.databyte = db
        self.parity = pr
        self.stopbits = sb
        self.timeout = to

    def getpath(self) :
        return self.devpath
    def getbr(self) :
        return self.baudrate
    def getdb(self) :
        return self.databyte
    def getpr(self) :
        return self.parity
    def getsb(self) :
        return self.stopbits
    def getto(self) :
        return self.timeout

def OpenSerial(dev_para) :
    logger_uart.info('into Serial Open function')
    logger_uart.warning('dev : {:s},\n Baudrate : {:d},\n Datalength : {:d},\n Parity : {:s},\n Stopbit : {:d},\n Timeout : {:f}ms\n'.format(dev_para.getpath(),
                        dev_para.getbr(), dev_para.getdb(), dev_para.getpr(), dev_para.getsb(), dev_para.getto() * 1000))
    if dev_para.getpr() == 'O' or dev_para.getpr() == 'o' :
        sparity = serial.PARITY_ODD
    elif dev_para.getpr() == 'E' or dev_para.getpr() == 'e' :
        sparity = serial.PARITY_EVEN
    else :
        sparity = serial.PARITY_NONE

    if dev_para.getsb() == 1 :
        sstop = serial.STOPBITS_ONE
    elif dev_para.getsb() == 1.5 :
        sstop = serial.STOPBITS_ONE_POINT_FIVE
    else :
        sstop = serial.STOPBITS_TWO

    if dev_para.getdb() == 5 :
        sbit = serial.FIVEBITS
    elif dev_para.getdb() == 6 :
        sbit = serial.SIXBITS
    elif dev_para.getdb() == 7 :
        sbit = serial.SEVENBITS
    else :
        sbit = serial.EIGHTBITS

    if dev_para.getbr() < 9600 :
        sbaud = 9600
    elif dev_para.getbr() > 115200 :
        sbaud = 115200
    else :
        sbaud = dev_para.getbr()
    return serial.Serial(dev_para.getpath(), baudrate = sbaud, bytesize = sbit, parity = sparity, stopbits = sstop, timeout = dev_para.getto())
