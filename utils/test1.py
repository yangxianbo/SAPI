#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-07-07 11:04:54
#FILENAME: test.py
#DESCRIPTION: 
#===============================================================

import time
t_name=time.strftime("%H%M%S", time.localtime())
new_file=file("/tmp/%s"%t_name,"w")
new_file.write(t_name+"\n")
new_file.close()
