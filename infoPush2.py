'''
Created on 2015年10月28日
infoPush的升级版，在使用中发现河畔的最新发表页不能及时更新
所以改为从主页的最新发表版块获取最新发表的帖子
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
from qshp.loginqshp import updateCookie
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
updateCookie(header, cookiePath)
keyword='自行车'
toaddrs=['1845585880@qq.com']
print('Keyword:'+keyword+'\nService for:\n'+str(toaddrs))
opener=getOpenerWithCookie(cookiePath)
message=''
threadIdSet=set()
sentThreadIdSet=set()#已发送的帖子，避免重发
#从txt文件中读取html内容
# htmlFile=codecs.open("htmlDoc.txt","r","utf-8")#F:/百度云同步盘/WorkDocument/Eclipse/NetCrawler/src/qshp
# html=htmlFile.read()
while 1:
    print(time.ctime()+" Start refreshing......")
    try:
        page=opener.open("http://bbs.uestc.edu.cn/")
        html=ungzip(page.read()).decode("utf-8","ignore")# ignore 表示忽略解码过程中遇到的非法字符
#        print(html)
    except Exception as e:
        print("Open page falure.")
        print(e)
    soup=BeautifulSoup(html,"html.parser")
    threadlist=soup.find("div",id="portal_block_67_content").find_all("li")
    for thread in threadlist:
        a=thread.find_all("a")[1]#a包含标题的<a herf="....." title="帖子标题">帖子标题</a>标签
        link=a["href"]#帖子对应的链接
        threadid=re.compile(r'http://.*tid=(.*)').findall(link)[0]
        title=a["title"]#帖子的标题
        if len(re.compile('.*'+keyword+'.*').findall(title))>0 and threadid not in sentThreadIdSet:
            message=message+"Title: "+title+"\n link: "+link+"\n"
            threadIdSet.add(threadid)
            sentThreadIdSet.add(threadid)
    if len(threadIdSet)>=1:#当搜集到的帖子超过5篇时，发送到邮箱
        sendEmail(toaddrs, message)
        print(time.ctime()+'  Messages have sent to:\n'+str(toaddrs))
        message=''
        threadIdSet.clear()
    time.sleep(3600*0.5)#每隔0.5小时刷新一次

# page=opener.open("http://bbs.uestc.edu.cn/")
# html=ungzip(page.read()).decode("utf-8","ignore")# ignore 表示忽略解码过程中遇到的非法字符
# print(html)
# soup=BeautifulSoup(html,"html.parser")