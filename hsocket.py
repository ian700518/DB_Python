#!/usr/bin/python3

import socket
import logging
import json
import time
import select
import threading
from string_utils import *
from bt import FILESIZE

logger_sock = logging.getLogger('SOCK_LOG')

class dbthread(threading.Thread) :
    def __init__(self, threadID, name, addressname, portnum) :
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.addressname = addressname
        self.portnum = portnum

    def run(self) :
        logger_sock.info('Thread Start : {}'.format(self.name))
        Connect2Ser(self.addressname, self.portnum)

def Connect2Ser(HostAddr, HostPort) :
    logger_sock.info('into Connect to Server function~~!!')
    Sendct = 0
    Current = time.time()
    Present = Current
    rxbuf = []
    while 1 :
        if Current - Present > 10 :
            Current = time.time()
            Present = Current
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if is_ip(HostAddr) == True :
                Host = HostAddr
            else :
                Host = socket.gethostname(HostAddr)
            try :
                s.connect((Host, HostPort))
                while 1 :
                    sock_readable, sock_writable, sock_exception = select.select([s], [s], [], 30)
                    if sock_readable :
                        try :
                            Sock_Str = s.recv(1024)
                            rxbuf.append(Sock_Str.decode('utf-8'))
                            logger_sock.warning('Sock_Str : {}, rxbuf is {}'.format(Sock_Str.decode('utf-8'), rxbuf))
                        except socket.error as err_msg :
                            logger_sock.error('Socket receive data error, {}'.format(err_msg))
                            break
                    else :
                        if sock_writable :
                            if len(rxbuf) > 0 :
                                with open('/DaBai/python/HostDeviceInfo.json', 'r') as fp :
                                    while 1 :
                                        filebuf = fp.read(FILESIZE)
                                        if filebuf != '' :
                                            try :
                                                Sendct += s.send(bytes(filebuf, 'utf8'))
                                                logger_sock.warning('Send buf is {}'.format(filebuf))
                                                logger_sock.warning('Send total count is {}'.format(Sendct))
                                            except socket.error as err_msg :
                                                logger_sock.error('Socket receive data error, {}'.format(err_msg))
                                                break
                                        else :
                                            break
                        break
                Sendct = 0
                rxbuf = []
            except socket.error as msg :
                logger_sock.error('Could not connect to server error msg {} ~~~!!!'.format(msg))
            s.close()
        else :
            Current = time.time()
