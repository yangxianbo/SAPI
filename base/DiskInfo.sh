#!/bin/bash
if [ -z `rpm -qa|grep Lib_Utils` ];then
	wget --http-user=Gvtv_stearm --http-password=gvtv_stearm http://d.listitv.com:9001/download/ppp/Lib_Utils-1.00-09.noarch.rpm -O  /home/work/software/Lib_Utils-1.00-09.noarch.rpm > /dev/null 2>&1
fi

if [ -z `rpm -qa|grep MegaCli` ];then
wget --http-user=Gvtv_stearm --http-password=gvtv_stearm http://d.listitv.com:9001/download/ppp/MegaCli-8.04.07-1.noarch.rpm -O  /home/work/software/MegaCli-8.04.07-1.noarch.rpm > /dev/null 2>&1
fi

rpm -ivh /home/work/software/Lib_Utils-1.00-09.noarch.rpm > /dev/null 2>&1
sleep 1
rpm -ivh /home/work/software/MegaCli-8.04.07-1.noarch.rpm > /dev/null 2>&1


if [ ! -h /usr/bin/megacli ];then
  if [ -f /opt/MegaRAID/MegaCli/MegaCli ];then
    ln -sf /opt/MegaRAID/MegaCli/MegaCli /usr/bin/megacli
  else
    ln -sf /opt/MegaRAID/MegaCli/MegaCli64 /usr/bin/megacli
  fi
fi

/usr/bin/megacli -cfgdsply -aALL | grep Inquiry|awk '{print $3"_"$4}'
