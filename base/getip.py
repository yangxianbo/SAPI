#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-08-17 16:26:30
#FILENAME: getip.py
#DESCRIPTION: 
#===============================================================


import socket
import fcntl
import struct
import commands
  
class RealIP():
    def __init__(self):
        self.device_list=commands.getoutput('ls /sys/class/net/').split('\n')
        self.device_list.remove('lo')
        
    def get_ip_address(self,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, 
            struct.pack('256s', ifname[:15])
        )[20:24])

    def ip_into_int(self,ip):
        return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

    def is_internal_ip(self,ip):
        ip = self.ip_into_int(ip)
        net_a = self.ip_into_int('10.255.255.255') >> 24
        net_b = self.ip_into_int('172.31.255.255') >> 20
        net_c = self.ip_into_int('192.168.255.255') >> 16
        return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

    def _start(self):
        ip_list=[]
        for device in self.device_list:
            try:
                ip_list.append(self.get_ip_address(device))
            except IOError:
                continue
        return ip_list

    def _check(self):
        check_list=self._start()
        result={}
        for check in check_list:
            result[check]=(self.is_internal_ip(check))
        return result

    def _run(self):
        n=0
        result=self._check()
        for key,value in result.items():
            if value == False:
                n += 1
        if n != 0:
            return "short"
        else:
            return "long"


if __name__ == "__main__":
    a=RealIP()
    print a._run()
    print a._start()
