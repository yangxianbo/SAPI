#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2016-05-04 10:59:18
#FILENAME: getsize.py
#DESCRIPTION: 
#===============================================================
from __future__ import division

import os,sys

def getsize(filename):
    size=float('%0.1f'%(os.path.getsize(filename)/1024/1024))
    return "%sM"%size
if __name__ == "__main__":
    if len(sys.argv[1:]) >= 1:
        filename=sys.argv[1]
        getsize(filename)
