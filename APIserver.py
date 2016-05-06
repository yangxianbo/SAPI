#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-06-19 17:13:49
#FILENAME: APIserver.py
#DESCRIPTION: 
#===============================================================


import SimpleXMLRPCServer
import os,sys,time,re
import string,socket
from daemon import Daemon
from APItransfer import api_transfer
from transfile import savefile
from utils.Scan_file import scan_file

socket.setdefaulttimeout(5)


accessList=(
    "127.0.0.1",
    "10.0.2.22",
    )

class APIserver(SimpleXMLRPCServer.SimpleXMLRPCServer):
    def __init__(self,*args):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self,(args[0],args[1]))

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SimpleXMLRPCServer.SimpleXMLRPCServer.server_bind(self)

    def verify_request(self,request, client_address):
        if client_address[0] in accessList:
            return 1
        else:
            return 0

def _start():
    server = APIserver('',19999)
    #注册函数
    server.register_function(api_transfer)
    server.register_function(scan_file)
    server.register_function(savefile)
    server.serve_forever()


def python_check():
    import platform
    if int(platform.python_version().replace('.','')) < 272:
        print 'Python 版本必须大于2.7.2'
        sys.exit()

class MyDaemon(Daemon):
    def run(self):
        _start()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-api.pid')
    python_check()
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
