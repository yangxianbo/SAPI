#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-06-24 10:01:35
#FILENAME: deco.py
#DESCRIPTION: 
#===============================================================


def hello(func):
     def echo_hello(*args, **kwargs):
        n=0
        for k in args:
            if k=='server':
                n+=1
                pid=12345
                func(*args, **kwargs)
            else:continue
        if n != 1:
            print "exit"
            sys.exit("%s"%args[0])
@hello
def echo(server):
    print pid
        

        
