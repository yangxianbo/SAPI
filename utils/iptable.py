#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2016-02-16 10:29:54
#FILENAME: iptable.py
#DESCRIPTION: 
#===============================================================

import commands
import sys
import re

class init_iptable():
    def __init__(self,ip,status):
        self.ip=ip
        self.status=status
        self.iptable_list=commands.getoutput('/sbin/iptables -nL').split('\n')
        
    def contrl_iptable(self):
        check_status=self._check_exist()
        add_msg="/sbin/iptables -A INPUT -s %s/32 -j DROP"%self.ip
        del_msg="/sbin/iptables -D INPUT -s %s/32 -j DROP"%self.ip
        if self.status=="0":
            if check_status == 0:
                print "add"
                commands.getoutput(add_msg)
        elif self.status=="1":
            if check_status == 1:
                print "del"
                commands.getoutput(del_msg)

    def _check_exist(self):
	n=0
        check_ip=re.compile(self.ip)
        for line in self.iptable_list:
            if len(check_ip.findall(line)) != 0:
                n+=1
                return 1
            else:
                pass
        if n==0:
            return 0

if __name__ == '__main__' :
    if len(sys.argv[1:]) >= 1:
        ip=sys.argv[1]
        status=sys.argv[2]
        Tb=init_iptable(ip,status)
        Tb.contrl_iptable()
