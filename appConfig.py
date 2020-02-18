from enum import Enum

services = ['getListByCountryTypeService2', 'getWikiList', 'getIndexRumorList',
            'getIndexRecommendList', 'getTimelineService', 'getStatisticsService',
            'getListByCountryTypeService1', 'getAreaStat', 'getEntries']

Service_host = 'https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0'

REMOTE_HOST = "https://pyecharts.github.io/assets/js"


class ApiError(Enum):
    API_TYPE_ERROR = (-1,"api not spport")
    JSON_EXCEPTION = (-2,"json parse error")
    SOURCE_FILE_NOT_EXISTS = (-3,"data source not exists")
    MAP_NOT_EXISTS = (-4,'dynamci nap not exists')
    UNKNOWN_ERROR = (-10,'unknown error')



class JobConfig(object):
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'updateInfo',  # 任务唯一ID
            'func': 'app.jobs:getInfo',
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': (Service_host,),  # 如果function需要参数，就在这里添加
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 60 * 20,
        }
    ]
