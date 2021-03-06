#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-08-21 11:45:37
#FILENAME: LongClient.py
#DESCRIPTION: 
#===============================================================


import socket
import time
import json
import sys
from base.getip import RealIP
from APItransfer import api_transfer
from daemon import Daemon
 
import logging
import logging.config

logging.config.fileConfig("./config/logging.conf")
logger = logging.getLogger("MyLogHandler")

def _start():
    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error, msg:
        logger.error(msg)
 
    try:
        connFd.connect(("127.0.0.1", 2003))
#        connFd.connect(("113.105.248.46", 2003))
        logger.info("connect to network server success")
    except socket.error,msg:
        logger.error(msg)

    messages={}
    messages['data']="heartbeat"
    get_ip=RealIP()
    messages['ip']=get_ip._start()[0]
    messages['key']="6af50cd1e1d57ffc845ecb157c8faf01"
    
 
    while 1:
        data=json.dumps(messages)
        if connFd.send(data) != len(data):
            logger.error("send data to network server failed")
            break
        messages['data']="heartbeat"
        readData = connFd.recv(1024)
        if readData != "heartbeat":
            recvData=json.loads(readData)
            if recvData['func'] == 'api_transfer':
                messages['data']=apit_transfer(json.dumps(recvData['msg']))
                logger.info("recevice msg:%s"%readData)
        else:
            logger.debug("receive heartbeat")
            time.sleep(5)
 
    connFd.close()

class MyDaemon(Daemon):
    def run(self):
        _start()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-Longclient.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.stop()
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

