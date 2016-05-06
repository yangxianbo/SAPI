#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2016-02-18 09:26:39
#FILENAME: control_iptable.py
#DESCRIPTION: 
#===============================================================


import commands
import sys

def iptable_commands(command):
    download_url="http://init.quliebiao.com:9011/initdown"
    d_user="inituser"
    d_passwd="initpwd"
    if command == "init":
        commands.getoutput("wget -T 8 -t 5 --http-user=%s --http-password=%s %s/iptable/iptables -O /etc/sysconfig/iptables")
        commands.getoutput("/sbin/service iptables restart")
        return 0
    elif command == "stop":
        commands.getoutput("/sbin/service iptables stop")
        return 0
    else:return -1
if __name__ == "__main__" :
    if len(sys.argv[1:]) >= 1:
        iptable_commands(sys.argv[1])
