#!/usr/bin/python
# -*- coding: UTF-8 -*- 
#coding:utf8
import smtplib
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
import os,sys,time,socket,fcntl,struct,pwd,psutil

def get_ip_address(ifname): 
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
   inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
   ret = socket.inet_ntoa(inet[20:24])  
   return ret  
    
# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
 
# Return RAM information (unit=kb) in a list                                       
# Index 0: total RAM                                                               
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 
# Return % of CPU used by user as a character string                                
def getCPUuse():
  return(str(psutil.cpu_percent(1))+"%")	
 
# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                         
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])


def senmail():    
    #---Process Email---
    NowDate = time.strftime('%Y.%m.%d %H:%M:%S')
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    ip = get_ip_address('wlan0')
    os_info = os.uname()
    #login_name = os.getlogin()
    login_name = pwd.getpwuid(os.geteuid()).pw_name

# CPU informatiom
    CPU_temp = getCPUtemperature()
    CPU_usage = getCPUuse()

# RAM information
# Output is in kb, here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)
    
    RAM_stats = str(RAM_stats)+'MB'
    RAM_total = str(RAM_total)+'MB'
    RAM_used = str(RAM_used)+'MB'
    RAM_free = str(RAM_free)+'MB'
 
# Disk information
    DISK_stats = getDiskSpace()
    DISK_total = DISK_stats[0]
    DISK_used = DISK_stats[1]
    DISK_perc = DISK_stats[3]
    
    DISK_stats = str(DISK_stats)+'B'
    DISK_total = str(DISK_total)+'B'
    DISK_used = str(DISK_used)+'B'
    DISK_perc = str(DISK_perc)

    TO = 'lilo.zhu@msn.com;lilo.zhu@qq.com;wei.zhu@osram.com'

    mail_content = """    
    <body>
    <table width="800" border="1" cellspacing="0" cellpadding="4">
    <tr>
        <td bgcolor="#CECFAD" height="20" style="font-size:16px; font-weight: bold;">* Raspberry Pi B3 Service Restart <a
        href="http://www.idev01.com:8080/myiot/tb_temperature.php"> More>></a></td>
    </tr>
    <tr>
        <td bgcolor="#EFEBDE" height="100" style="font-size:13px">
            <table style="font-weight: bold" border="1" cellspacing="0" cellpadding="1">
                <tr><td>DateTime:</td>
                    <td>%s</td>
                </tr>
                <tr><td>HostName:</td>
                    <td>%s</td>
                </tr>
                <tr><td>IP:</td>
                    <td>%s</td>
                </tr>
                <tr><td>OS Info:</td>
                    <td>%s</td>
                </tr>
                <tr><td>Login Name:</td>
                    <td>%s</td>
                </tr>
                <tr><td>CPU Temperature:</td>
                    <td>%s</td>
                </tr>
                <tr><td>CPU Use:</td>
                    <td>%s</td>
                </tr>
                <tr><td>RAM Total:</td>
                    <td>%s</td>
                </tr>
                <tr><td>RAM Used :</td>
                    <td>%s</td>
                </tr>
                <tr><td>RAM Free :</td>
                    <td>%s</td>
                </tr>
                <tr><td>DISK Total Space:</td>
                    <td>%s</td>
                </tr>
                <tr><td>DISK Used Space:</td>
                    <td>%s</td>
                </tr>
                <tr><td>DISK Used Percentage:</td>
                    <td>%s</td>
                </tr>
            </table>
        </td>
    </tr>
    </table>
    """ % (NowDate,hostname,ip,os_info,login_name,CPU_temp,CPU_usage,RAM_total,RAM_used,RAM_free,DISK_total,DISK_used,DISK_perc)

    # email Sign In
    SUBJECT = "Notice: [" + hostname + "] shell service restart ---"+ NowDate
    email_sender = 'lilo.zhu@msn.com'
    email_passwd = 'Osram9809'

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_sender, email_passwd)

    subject = SUBJECT  
    msg = MIMEText(mail_content,'html','utf-8')    
    msg['Subject'] = subject  
    msg['Accept-Language']='zh-CN'
    msg['Accept-Charset']='ISO-8859-1,utf-8'
    msg['to'] = TO
    # msg['Cc'] = acc
    msg['from'] = email_sender

    reload(sys)
    sys.setdefaultencoding('gb18030')
    server.sendmail(email_sender, TO.split(';'), msg.as_string())
    server.quit()
     
if __name__ == '__main__':
   senmail()
