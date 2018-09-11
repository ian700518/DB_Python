#!/usr/bin/python

import subprocess

def Send_Command(command) :
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
    return p.stdout.read()
