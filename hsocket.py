#!/usr/bin/python3

import socket
import logging
import json
from string_utils import *
from bt import FILESIZE

logger_sock = logging.getLogger('SOCK_LOG')

def Connect2Ser(HostAddr, HostPort) :
    logger_sock.info('into Connect to Server function~~!!')

    Sendct = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if is_ip(HostAddr) == True :
        Host = HostAddr
    else :
        Host = socket.gethostname(HostAddr)
    while 1 :
        try :
            s.connect((Host, HostPort))
            break
        except socket.error as msg :
            logger_sock.error('Could not connect to server error msg {} ~~~!!!'.format(msg))

    with open('/DaBai/python/HostDeviceInfo.json', 'r') as fp :
        while 1 :
            filebuf = fp.read(FILESIZE)
            if filebuf != '' :
                Sendct += s.send(bytes(filebuf, 'utf8'))
                logger_sock.warning('Send buf is {}'.format(filebuf))
                logger_sock.warning('Send total count is {}'.format(Sendct))
            else :
                break
