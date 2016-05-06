#!/usr/bin/python2.7
#coding:utf-8
#AUTHOR: yangxb
#CREATER: 2015-06-22 15:00:12
#FILENAME: trans_control.py
#DESCRIPTION: 
#===============================================================


import commands
import sys,os
import time
import send_query

class Check_transcoder:
    def __init__(self,checkname):
        if checkname == "server" or checkname == "client":
            self.checkname = checkname
        else:
            sys.exit(-1000)
                
    def check_process(self):
        process_dic={}
        check_daemon_dic={}
        check_server_dic={}

        if self.checkname == "server":
            check_daemon=commands.getoutput("ps aux|grep run_server|grep -v grep").split()
            check_server=commands.getoutput('''ps aux|grep server|grep -v -E "grep|run_server" ''').split()
            
            if check_daemon != []:
                check_daemon_dic['uptime']=check_daemon[8]
                check_daemon_dic['pid']=check_daemon[1]
                check_server_dic['uptime']=check_server[8]
                check_server_dic['pid']=check_server[1]

                process_dic['daemon']=check_daemon_dic
                process_dic['server']=check_server_dic
                return process_dic
            else:
                return -1001

        elif self.checkname == "client":
            
            check_daemon=commands.getoutput("ps aux|grep run_tc|grep -v grep").split()
            check_server_uptime=commands.getoutput("ps aux -ejH|grep transcoder|grep -v grep|awk '{print $11}' ").split('\n')
            check_server_pid=commands.getoutput("ps aux -ejH|grep transcoder|grep -v grep|awk '{print $2}'").split('\n')

            if check_daemon != []:
                check_daemon_dic['uptime']=check_daemon[8]
                check_daemon_dic['pid']=check_daemon[1]
                check_server_dic['uptime']=check_server_uptime[0]
                check_server_dic['pid']=check_server_pid

                process_dic['daemon']=check_daemon_dic
                process_dic['server']=check_server_dic
                if len(check_server_pid) > 1:
                    process_dic['task_id']=self._check_task()
                return process_dic
            else:
                return -1002

    def start_process(self):
        process_dic=self.check_process()
        if isinstance(process_dic, dict):
            return -1003
        if self.checkname == "server":
            os.system("cd /opt/Transtool_Server && nohup ./run_server.sh >/dev/null & ")
            return 0
        elif self.checkname == "client":
            os.system('''cd /opt/Transtool_Transcoder && nohup ./run_tc.sh >/dev/null  &''')
            return 0

    def stop_process(self):
        process_dic=self.check_process()
        if not isinstance(process_dic, dict):
            return -1004
        if self.checkname == "server":
            kill_list=[process_dic['daemon']['pid'],process_dic['server']['pid']]
            for pid in kill_list:
                os.system("kill -9 %s"%pid)
                time.sleep(1)
            return 0
        elif self.checkname == "client":
            kill_list=[]
            kill_list.append(process_dic['daemon']['pid'])
            for i in process_dic['server']['pid']:
                kill_list.append(i)
            for pid in kill_list:
                os.system("kill -9 %s"%pid)
                time.sleep(1)
            return 0
            

    def restart_process(self):
        if self.stop_process() != 0:
            return -1005
        self.start_process()
        return 0

    def _check_task(self):
        task_id=commands.getoutput('''cat /tmp/translog/debug_log.txt|grep "task_id is"|tail -n1|awk '{print $NF}' ''')
        return task_id
        

if __name__ == "__main__":
    checkname,process=sys.argv[1:] 
    trans=Check_transcoder(checkname)
    if process == 'start':
        trans.start_process()
    elif process == 'stop':
        trans.stop_process()
    elif process == 'restart':
        trans.restart_process()
    elif process == 'check':
        status=trans.check_process()

