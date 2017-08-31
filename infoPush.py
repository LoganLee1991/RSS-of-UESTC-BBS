'''
Created on 2015年10月22日
学习用BeautifulSoup提取HTML的内容
实现了根据关键词从河畔的最新发表页面搜索相关的帖子
这是tryBS的升级版，不依赖apcheduler，当相关帖子数达到一定数量时自动发送邮件
@author: LeeHui
'''
#from qshp.loginqshp import html #会完整运行loginqshp中的所有代码
import codecs
import re
import time
import socket

from bs4 import BeautifulSoup
from qshp.loginqshp import getOpenerWithCookie  # 会完整运行loginqshp中的所有代码
from qshp.loginqshp import ungzip
from qshp.sendMessage import sendEmail

socket.setdefaulttimeout(30)
#用cookie信息打开河畔网页
header={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.33 Safari/537.36"
        }
cookiePath="./cookie.txt"
# updateCookie(header, cookiePath)
keyword='offer'
toaddrs=['1845585880@qq.com']
print('Keyword:'+keyword+'\nService for:\n'+str(toaddrs))
opener=getOpenerWithCookie(cookiePath)
message=''
threadIdSet=set()
while 1:
    #从txt文件中读取html内容
    # htmlFile=codecs.open("htmlDoc.txt","r","utf-8")#F:/百度云同步盘/WorkDocument/Eclipse/NetCrawler/src/qshp
    # html=htmlFile.read()
    print(time.ctime()+" Start refreshing......")
    page=opener.open("http://bbs.uestc.edu.cn/forum.php?mod=guide&view=newthread")
    html=ungzip(page.read()).decode("utf-8","ignore")# ignore 表示忽略解码过程中遇到的非法字符
    soup=BeautifulSoup(html,"html.parser")
    threadlist=soup.find("div",id="forumnew").parent.find_all("tbody")
    for thread in threadlist:
        threadid=thread["id"]
        a=thread.find("th").find("a")#a包含标题的<a herf=".....">帖子标题</a>标签
        link=a["href"]#帖子对应的链接
        title=a.string#帖子的标题
        if len(re.compile('.*'+keyword+'.*').findall(title))>0 and threadid not in threadIdSet:
            message=message+"Title: "+title+"\n link: "+link+"\n"
            threadIdSet.add(threadid)
    if len(threadIdSet)>=5:#当搜集到的帖子超过5篇时，发送到邮箱
        sendEmail(toaddrs, message)
        print(time.ctime()+'  Messages have sent to:\n'+str(toaddrs))
        message=''
        threadIdSet.clear()
    time.sleep(3600*6)#每隔6小时刷新一次