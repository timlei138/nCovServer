from flask import Flask
# 引用 APSchedule
from flask_apscheduler import APScheduler
#
import atexit
import fcntl
import json

# 引用 congfig 配置
from appConfig import  JobConfig
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
app.config.from_object(JobConfig)
if __name__ == 'app':
    f = open('scheduler.lock','wb')
    try:
        fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
    except:
        print("scheduler locked,pass")
        pass
    def unlock():
        fcntl.flock(f,fcntl.LOCK_UN)
        f.close()
    atexit.register(unlock)


#如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了
from app import routes


