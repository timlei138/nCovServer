# 从app模块中即从__init__.py中导入创建的app应用
from app import app
from app import jobs


# 建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。
@app.route('/')
def index():
    return "2019 流感病毒数据，数据来源于丁香医生。请勿做非法使用"


@app.route('/api/getListByCountryTypeService2', methods=['GET', 'POST'])
def getListByCountryType2():
    return jobs.getJsonInfo('getListByCountryTypeService2')


@app.route('/api/getWikiList', methods=['GET', 'POST'])
def getWikis():
    return jobs.getJsonInfo('getWikiList')


@app.route('/api/getIndexRumorList', methods=['GET', 'POST'])
def getIndexRumors():
    return jobs.getJsonInfo('getIndexRumorList')


@app.route('/api/getIndexRecommendList', methods=['GET', 'POST'])
def getIndexRecommends():
    return jobs.getJsonInfo('getIndexRecommendList')


@app.route('/api/getTimelineService', methods=['GET', 'POST'])
def getTimeLine():
    return jobs.getJsonInfo('getTimelineService')


@app.route('/api/getStatisticsService', methods=['GET', 'POST'])
def getStatistics():
    return jobs.getJsonInfo('getStatisticsService')


@app.route('/api/getListByCountryTypeService1', methods=['GET', 'POST'])
def getListByCountryType1():
    return jobs.getJsonInfo('getListByCountryTypeService1')


@app.route('/api/getAreaStat', methods=['GET', 'POST'])
def getAreaStat():
    return jobs.getJsonInfo('getAreaStat')


@app.route('/api/getEntries', methods=['GET', 'POST'])
def getEntries():
    return jobs.getJsonInfo('getEntries')


@app.route('/api/getDynamicMap',methods=['GET'])
def getGetDynamcicMap():
    return jobs.getDynamicMapUrl()