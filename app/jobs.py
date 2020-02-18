# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from appConfig import services
from appConfig import ApiError
from flask import Response
from pyecharts import Map
from flask import url_for

api_dict_common = {
    'version': '1.0',
    'update': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
    'errorCode': 0,
    'errorMsg': ''
}

json_root = os.getcwd() + '/info/'


def getInfo(url):
    print('open url ->', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        'Cookie': 'ASP.NET_SessionId=yolmu555asckw145cetno0um'
    }
    strhtml = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(strhtml.content.decode('utf-8'), 'lxml')
    dataList = {}
    for service in services:
        dataText = soup.select('#' + service)
        print("dataText", dataText)
        tags = dataText.pop()
        for tag in tags:
            text = tag.string[tag.string.index('=') + 1:tag.string.rindex('}') - 10].lstrip()
            data = json.loads(text)
            dataList[service] = data

    print('rootPath:', json_root)
    if os.path.exists(json_root) and os.path.isdir(json_root):
        pass
    else:
        os.mkdir(json_root)
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    api_dict_common['update'] = curr_time
    for info in dataList:
        data = dataList[info]
        api_dict_common['data'] = data
        api_dict_common['errorCode'] = 0
        api_dict_common['errorMsg'] = ''
        json_str = json.dumps(api_dict_common, ensure_ascii=False)
        with open(os.path.join(json_root, info + ".json"), 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)

    province_list = dataList['getAreaStat']
    if province_list is not None:
        drawVirusMap('全国疫情地图', "数据更新时间:" + curr_time, province_list)


def getDynamicMapUrl():
    url = url_for('static', _external=True, filename='dynamic_map/epidemic_map.png')
    api_dict_common['update'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if url.strip() == '':
        return getErrorResponse(ApiError.MAP_NOT_EXISTS)
    else:
        api_dict_common['data'] = {'url': url}
        api_dict_common['errorCode'] = 0
        api_dict_common['errorMsg'] = ''
    return Response(json.dumps(api_dict_common, ensure_ascii=False), mimetype='application/json');


def getJsonInfo(api_type):
    if api_type not in services:
        return getErrorResponse(ApiError.API_TYPE_ERROR)
    json_file = json_root + api_type + '.json'
    print(json_file)
    if os.path.exists(json_file):
        try:
            jsonFile = open(json_file, 'r', encoding='UTF-8')
            jsonDict = json.load(jsonFile)
            # print("query:"+json.dumps(jsonDict, ensure_ascii=False))
            response = Response(json.dumps(jsonDict, ensure_ascii=False), mimetype='application/json')
            return response
        except:
            return getErrorResponse(ApiError.JSON_EXCEPTION)
    else:
        return getErrorResponse(ApiError.SOURCE_FILE_NOT_EXISTS)


def drawVirusMap(title, update, data):
    print('make up  update time data =>', update)
    privinces = []
    values = []
    for item in data:
        privinces.append(item['provinceShortName'])
        values.append(item['currentConfirmedCount'])
    virus_map = Map(title, update, title_color='#0E1116', title_pos='center',
                    title_text_size=18.0, width=1280, height=960, subtitle_color='#808080')
    virus_map.add("当前确诊", privinces, values, "china", is_label_show=True, label_text_size=10,
                  is_legend_show=False, is_visualmap=True, visual_top='bottom', is_calculable=True,
                  is_piecewise=True, visual_range_text=['', ''], pieces=[
            {'min': 10000, 'label': '>10000', 'color': '#4F070D'},
            {'min': 1000, 'max': 10000, 'label': '1000-10000', 'color': '#811C24'},
            {'min': 500, 'max': 999, 'label': '500-999', 'color': '#CB2A2F'},
            {'min': 100, 'max': 499, 'label': '100-499', 'color': '#E55A4E'},
            {'min': 10, 'max': 99, 'label': '10-99', 'color': '#F59E83'},
            {'min': 1, 'max': 9, 'label': '1-9', 'color': '#FDEBCF'},
            {'min': 0, 'max': 0, 'label': '0', 'color': '#FFFFFF'},
        ])
    virus_map.render(path='app/static/dynamic_map/epidemic_map.png')


def getErrorResponse(code):
    api_dict_common['data'] = None
    api_dict_common['errorCode'] = code.value[0]
    api_dict_common['errorMsg'] = code.value[1]
    return Response(json.dumps(api_dict_common), mimetype='application/json')
