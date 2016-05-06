#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-06-25 17:43:01
#FILENAME: APItransfer.py
#DESCRIPTION: 
#===============================================================


import logging
import logging.config

logging.config.fileConfig("./config/logging.conf")
logger = logging.getLogger("MyLogHandler")

import os,sys
import commands
import json

append_path=os.path.abspath('./')
sys.path.append(append_path)

dir_path_list=['utils']

def api_transfer(jsonstring):
    try:
        arg_dict=json.loads(jsonstring)
        if arg_dict.has_key('script') and arg_dict.has_key('args'):
            if isinstance(arg_dict['script'], unicode) and isinstance(arg_dict['args'], list):
                scriptname=arg_dict['script']
                arg_list=arg_dict['args']
                arg_str=''
                for arg in arg_list:
                    arg_str += ' "%s"'%str(arg)
                arg_str.strip("")
                n=0
                for path in dir_path_list:
                    file_path=os.path.join(append_path,path,scriptname)
                    if os.path.exists(file_path):
                       n+=1
                    else:continue
                if n==1:
                    script_type=scriptname.split('.')[-1]
                    if script_type == "sh":
                        run_str='sh %s %s'%(file_path,arg_str)
                        logger.info('RUN %s'%run_str)
                        os.system(run_str)
                        return 0
                    elif script_type == "py":
                        run_str='python2.7 %s %s'%(file_path,arg_str)
                        logger.info('RUN %s'%run_str)
                        os.system(run_str)
                        return 0
                    else:return -3001
                else:return -3002
            else:return -3003
        elif arg_dict.has_key("transfile") and arg_dict.has_key("status"):
            if isinstance(arg_dict['transfile'], list) and isinstance(arg_dict['status'], unicode):
                return "1"
                
        else:return -3004
                
    except ValueError:
        return -3000

