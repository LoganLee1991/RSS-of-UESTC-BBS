'''
Created on 2015年10月23日
定时运行程序
@author: LeeHui
'''
from qshp.tryBS import work
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.job import Job
import os
import apscheduler

keyword="offer"
toaddrs=['1845585880@qq.com']
scheduler=BlockingScheduler()
scheduler.add_job(work,'interval',seconds=3,args=[keyword,toaddrs],max_instances=3,misfire_grace_time=60)#第二个参数表示设置时间的方式。interval表示间隔一段时间执行一次,args为调用的函数的参数，可以为元组或list
# scheduler.add_job(work,'cron',day_of_week='7',hour='12',args=[keyword,toaddrs])#第二个参数表示设置时间的方式。cron可以比较随意地设置
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))#os.name字符串指示正在使用的平台,nt表示windows
print('Keyword:'+keyword+'\nService for:\n'+str(toaddrs))
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
