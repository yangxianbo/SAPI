#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-06-04 21:18:33
#FILENAME: check_hardware.py
#DESCRIPTION: 
#===============================================================


import commands,re,os,uuid,json
import send_query
import logging
import logging.config
from getip import RealIP

logging.config.fileConfig("../config/logging.conf")
logger = logging.getLogger("MyLogHandler")

class hardware():
    def __init__(self):
        if os.path.exists('/usr/sbin/dmidecode') == "Flase":
            logger.warning("dmidecode is not exists")
            logger.info("start install dmidecode...")
            result=commands.getstatusoutput('yum install -y dmidecode')[0]
            if result==0:
                logger.info("install dmidecode success")
            else:
                logger.warning("install dmidecode fail")
                sys.exit(-1000)
        else:
                pass

    def check_hardware(self):
        hardware_dict={}
        hardware_list=['system-serial-number','system-manufacturer','system-product-name','processor-version']
        for dmic in hardware_list:
            if dmic == "processor-version":
                cpu=commands.getoutput('''cat /proc/cpuinfo|grep "model name"|head -n1|awk -F ":" '{print $2}' ''').replace(" ","")
                cpu_num=commands.getoutput("dmidecode -s %s|wc -l"%dmic)
                cpu_info=cpu+" * "+cpu_num
                hardware_dict[dmic]=cpu_info
            else:
                keyword=commands.getoutput("dmidecode -s %s"%dmic).replace(" ","").replace("\n"," ")
                hardware_dict[dmic]=keyword.strip('.')

        hardware_dict['Disk_hardware']={}
        disk_list=commands.getoutput('''parted -l|grep scsi|awk -F ":" '{print $2}'|awk 'NF--' ''').split("\n")
        n=0
        for disk in disk_list:
            hardware_dict['Disk_hardware']["disk%s"%n]=disk
            n+=1

        hardware_dict['Disk_size']={}
        disk_part=commands.getoutput("parted -l|grep dev").replace('\n',' ') #防止中文模式导致无法过滤
        p2=re.compile(r'''.*?(/dev.*?):(.*?B)''')
        disk_source=p2.findall(disk_part)
        for disk in disk_source:
            hardware_dict['Disk_size'][disk[0]]=disk[1].strip()

        memory=float(commands.getoutput("cat /proc/meminfo |grep MemTotal|awk '{print $2}'"))/1048576
        memory=float('%0.0f'%memory)
        hardware_dict['Memory_total']="%s G"%memory
        
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
        mac_real=":".join([mac[e:e+2] for e in range(0,11,2)])
        hardware_dict['MAC']=mac_real
        def hostname():
            sys = os.name  
            if sys == 'nt':  
                hostname = os.getenv('computername')  
                return hostname  
            elif sys == 'posix':  
                hostname = commands.getoutput('hostname')
                return hostname  
            else:  
                return 'Unkwon hostname'
        local_name=hostname()
        hardware_dict['hostname']=local_name

        get_ip=RealIP()
        ip_type=get_ip._run()
        if ip_type == "long":
            hardware_dict['ip']=get_ip._start()[0]
            hardware_dict['type']="long"
        else:
            hardware_dict['type']="short"
        

        return hardware_dict


hd=hardware()
local_info=hd.check_hardware()

get_url="http://10.0.2.22:8000/hardware/api_hardware/"
post_url="http://10.0.2.22:8000/hardware/api_hardware/"
get_key="18ec65f8d56d090559dc6283a316b2c2"
post_key="c1d585bb2e4e5001e4a3d0371d9cb039"
get_dic={'key':get_key}
local_info['key']=post_key
get_info=json.loads(send_query.get_info(get_url,get_dic))

if get_info == {}:
    send_query.post_info(post_url,local_info)
else:
    local_list=[]
    get_list=[]
    for k,v in local_info.items():
        if k != 'key':
            local_list.append(v)
    for k,v in get_info['hardwareinfo'].items():
        if k != "ip":
            get_list.append(v)
    for i in get_list:
        if i not in local_list:
            try:
                if eval(i) not in local_list:
                    send_query.post_info(post_url,local_info)
            except NameError:
                if str(i) not in local_list:
                    send_query.post_info(post_url,local_info)
