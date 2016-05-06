#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2016-02-22 09:37:02
#FILENAME: transfile.py
#DESCRIPTION: 
#===============================================================

import logging
import logging.config
import time

logging.config.fileConfig("./config/logging.conf")
logger = logging.getLogger("MyLogHandler")

import os,json,pickle,commands
def savefile(jstring):
    def time_now():
        return time.strftime("%H%M%S", time.localtime())

    def writefile(filename,data,origin_md5):
        handle = open(filename, "wb")
        handle.write(pickle.loads(data))
        logging.info("write file:%s"%filename)
        handle.close()
        new_md5=commands.getoutput("md5sum %s"%filename).split(' ')[0]
        if new_md5 == origin_md5:
            return 0
        else:return -1

    try:
        fileinfo=json.loads(jstring) 
        error_list=[]
        redict={}
        for fname,fdata in fileinfo.items():
            dirname=os.path.dirname(fdata[1])
            getname=os.path.basename(fdata[1])
            if getname != '':
                filename = getname
            else:
                filename = os.path.basename(fname)
            basename="%s/%s"%(dirname,filename)

            if os.path.exists(dirname) == False:
                os.system("mkdir -p %s"%dirname)
                if writefile(basename,fdata[0],fdata[2]) != 0:
                    error_list.append(basename)
            else:
                if os.path.exists(basename):
                    ntime=time_now()
                    os.system("mv %s %s.%s"%(basename,basename,ntime))
                    if writefile(basename,fdata[0],fdata[2]) != 0:
                        error_list.append(basename)
                else:
                    if writefile(basename,fdata[0],fdata[2]) != 0:
                        error_list.append(basename)
        if error_list != []:
            redict['error']=error_list
            return json.dumps(redict)
        else:return 0

    except ValueError:
        return -3000
    

