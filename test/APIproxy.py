#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-06-19 17:48:42
#FILENAME: APIproxy.py
#DESCRIPTION: 
#===============================================================


from xmlrpclib import ServerProxy
import json
#a={"script":"trans_control.py","args":['client','start']}
a={"path_list":["/opt","/data/software"],"exclude":""}
a_json=json.dumps(a)
print a_json
s=ServerProxy('http://10.0.2.22:19999')
print s.scan_file(a_json)
