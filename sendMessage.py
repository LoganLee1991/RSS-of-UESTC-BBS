'''
Created on 2015年10月23日
用来将爬取到的信息发送到指定邮箱，实现信息推送功能
@author: LeeHui
'''
import smtplib
import email.mime.multipart
import email.mime.text
from email.utils import COMMASPACE,formatdate

#toaddrs：接收邮箱列表
#message：邮件内容
def sendEmail(toaddrs,message):
    msg=email.mime.multipart.MIMEMultipart()
    msg['from']='ylelh@sina.com'
    msg['to']=COMMASPACE.join(toaddrs)#COMMASPACE==', ' 
    msg['subject']='你关注的河畔帖子'
    msg['date']=formatdate(localtime=True)
    txt=email.mime.text.MIMEText(message)
    msg.attach(txt)
    
    smtp=smtplib.SMTP()
    smtp.connect('smtp.sina.com.cn', '25')
    smtp.login('ylelh@sina.com','712@sina')
    smtp.sendmail('ylelh@sina.com',toaddrs,str(msg))
    smtp.quit()
    return()
