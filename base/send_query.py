#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-06-10 17:07:33
#FILENAME: send_query.py
#DESCRIPTION: 
#===============================================================


import urllib
import urllib2
import json
import httplib
import logging
import logging.config

logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger("MyLogHandler")


def get_info(url,postinfo):
    getdata=urllib.urlencode(postinfo)
    req=urllib.urlopen("%s?%s"%(url,getdata))
    code=req.getcode()
    logger.info("GET %s to %s"%(getdata,url))
    return req.read()

def post_info(url,postinfo):
    jdata = json.dumps(postinfo)             # 对数据进行JSON格式化编码
    req = urllib2.Request(url, jdata)       # 生成页面请求的完整数据
    response = urllib2.urlopen(req)       # 发送页面请求
    logger.info("POST %s to %s"%(jdata,url))
    return response.read()                    # 获取服务器返回的页面信息

if __name__ == "__main__":
    post_info('http://dispmsg.gvppp.com:5208',{"action":"fetch_channel_status","group_id":1,"chn":0,"ip":""})
