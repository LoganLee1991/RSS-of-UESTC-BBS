'''
Created on 2015年10月8日
登陆清水河畔
@author: LeeHui
'''
import gzip
import http.cookiejar
import urllib.request
import re

#解压函数
def ungzip(data):#data需要decode
    try:        # 尝试解压
#         print('正在解压.....')
        data = gzip.decompress(data)
#         print('解压完毕!')
    except:
        pass
#         print('未经压缩, 无需解压')
    return(data)

#构造文件头
def getOpener(head):#一定要有cookie，不然会登陆失败
    cj=http.cookiejar.CookieJar()
    pro=urllib.request.HTTPCookieProcessor(cj)
    opener=urllib.request.build_opener(pro)
    header=[]
    for key,value in head.items():
        elem=(key,value)
        header.append(elem)
    opener.addheaders=header
    return opener

def getOpenerWithCookie(cookiePath):#一定要有cookie，不然会登陆失败
    cookie=http.cookiejar.MozillaCookieJar()
    cookie.load(cookiePath, ignore_discard=True, ignore_expires=True)#从文件中读取cookie
    pro=urllib.request.HTTPCookieProcessor(cookie)
    opener=urllib.request.build_opener(pro)
#     由于使用了cookie，所以不再需要header
#     header=[]
#     for key,value in head.items():
#         elem=(key,value)
#         header.append(elem)
#     opener.addheaders=header
    return opener

#通过登录获取河畔的cookie并保存至txt文件中
def updateCookie(head,cookiePath):#一定要有cookie，不然会登陆失败
    url="http://bbs.uestc.edu.cn/member.php?mod=logging&action=login"
    cookie=http.cookiejar.MozillaCookieJar()
    pro=urllib.request.HTTPCookieProcessor(cookie)
    opener=urllib.request.build_opener(pro)
    header=[]
    for key,value in head.items():
        elem=(key,value)
        header.append(elem)
    opener.addheaders=header
    loginPage=opener.open(url)
    loginPageHtml=ungzip(loginPage.read()).decode("utf-8","ignore")
    formhash=getFormhash(loginPageHtml)
    loginhash=getLoginhash(loginPageHtml)
#     print("formhash:"+formhash)
#     print("loginhash:"+loginhash)
      
    postDict={
              'formhash' : formhash,
              'referer' : 'http://bbs.uestc.edu.cn/index.php',
              'loginfield' : 'username',
              'username' : u'木子飞',
              'password' : '*******',
              'questionid' : 0,
              'answer' : '',
              'cookietime' : 2592000,
              'loginsubmit' : 'true'
              }
    #需要给Post数据编码
    postData=urllib.parse.urlencode(postDict).encode('utf-8')
#     print(postData)
    url=url+'&loginsubmit=yes&loginhash='+loginhash+'&inajax=1'#从fiddler上观察到登陆的信息被POST到这个链接中
#     print(url)
    opener.open(url,postData)#执行登陆过程，登陆成功
    cookie.save(cookiePath, ignore_discard=True, ignore_expires=True)
    return()

def getFormhash(htmlPage):#登陆页面每次刷新都有不同的formhash和loginhash
    reg=re.compile('name="formhash" value="(.*)"')
    strlist=reg.findall(htmlPage)
    return strlist[0]

def getLoginhash(htmlPage):
    reg=re.compile('loginhash=(.*)"')
    strlist=reg.findall(htmlPage)
    return strlist[0]
#----------------------------------------------------------------------
# header={
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Encoding": "gzip, deflate",
#         "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
#         "Upgrade-Insecure-Requests": 1,
#         "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.33 Safari/537.36"
#         }
# updateCookie(header, "cookie.txt")
#利用http.cookiejar.CookieJar()登录打开河畔首页
#从登陆页面获取formhash和loginhash
# url="http://bbs.uestc.edu.cn/member.php?mod=logging&action=login"
# opener=getOpener(header)
# loginPage=opener.open(url)
# loginPageHtml=ungzip(loginPage.read()).decode("utf-8","ignore")
# formhash=getFormhash(loginPageHtml)
# loginhash=getLoginhash(loginPageHtml)
# print("formhash:"+formhash)
# print("loginhash:"+loginhash)
#   
# postDict={
#           'formhash' : formhash,
#           'referer' : 'http://bbs.uestc.edu.cn/index.php',
#           'loginfield' : 'username',
#           'username' : u'木子飞',
#           'password' : '*******',
#           'questionid' : 0,
#           'answer' : '',
#           'cookietime' : 2592000,
#           'loginsubmit' : 'true'
#           }
# postData=urllib.parse.urlencode(postDict).encode('utf-8')
# print(postData)
# url=url+'&loginsubmit=yes&loginhash='+loginhash+'&inajax=1'#从fiddler上观察到登陆的信息被POST到这个链接中
# print(url)
# opener.open(url,postData)#执行登陆过程，登陆成功
# page=opener.open("http://bbs.uestc.edu.cn/index.php")#手动跳转到主页
# html=ungzip(page.read()).decode("utf-8","ignore")
# print(html)
#--------------------------------------------------------------------------------------------
#用cookie文件打开河畔首页
# cookiePath="cookie.txt"
# # updateCookie(header, cookiePath)
# opener=getOpenerWithCookie(cookiePath)
# page=opener.open("http://bbs.uestc.edu.cn/index.php")
# html=ungzip(page.read()).decode("utf-8","ignore")
# print(html)
 






        
    