# -*- coding: utf-8 -*-

import sys
import json,urllib
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

ROOT_CATEGORY_IDS={
    '动画':{'children':{
        '综合':27,
        'MAD*AMV':24,
        'MMD*3D':25,
        '动画短片':47,
    },'id':1,'thumbnail':'1','name':'动画'},
    '番剧':{'children':{
        '完结动画':32,
        '连载动画':33,
        '资讯':51,
        '官方衍生':152,
        '国产动画':153,
    },'id':2,'thumbnail':'2','name':'番剧'},
    '音乐':{'children':{
        '音乐选集':130,
        '同人音乐':28,
        '三次元音乐':29,
        'VOCALOID·UTAU':30,
        '翻唱':31,
        'OP/ED/OST':54,
        '演奏':59,
    },'id':3,'thumbnail':'3','name':'音乐'},
    '舞蹈':{'children':{
        'ACG相关舞蹈':20,
        '三次元舞蹈':154,
    },'id':4,'thumbnail':'4','name':'舞蹈'},
    '游戏':{'children':{
        '单机联机':17,
        'Mugen':19,
        '电子竞技':60,
        '网络游戏':65,
        'GMV':121,
        '音游':136,
    },'id':5,'thumbnail':'5','name':'游戏'},
    '科技':{'children':{
        '纪录片':37,
        '演讲公开课':39,
        '数码':95,
        '军事':96,
        '机械':98,
        '野生技术学会':122,
        '趣味科普人文':124,
    },'id':6,'thumbnail':'6','name':'科技'},
    '娱乐':{'children':{
        '美食圈':76,
        '动物圈':75,
        '综艺':71,
        '生活':21,
        '搞笑':138,
        '娱乐圈':137,
        'korea相关':131,
    },'id':7,'thumbnail':'7','name':'娱乐'},
    '鬼畜':{'children':{
        '三次元鬼畜':22,
        '二次元鬼畜':26,
        '人力vocaloid':126,
        '教程演示':127,
    },'id':8,'thumbnail':'8','name':'鬼畜'},
    '电影':{'children':{
        '电影相关':82,
        '其他国家':83,
        '短片':85,
        '欧美电影':145,
        '日本电影':146,
        '国产电影':147,
    },'id':9,'thumbnail':'9','name':'电影'},
    '电视剧':{'children':{
        '连载剧集':15,
        '完结剧集':34,
        '特设布袋':86,
        '电视剧相关':128,
    },'id':10,'thumbnail':'10','name':'电视剧'}
}
def find_id_in_category_ids(id):
    for i in ROOT_CATEGORY_IDS:
        for j in ROOT_CATEGORY_IDS[i]['children']:
            print j
            print ROOT_CATEGORY_IDS[i]['children'][j]


#print find_id_in_category_ids(1)



def get_tag_category():
    url="http://www.bilibili.com/index/catalog_tags.json"
    r = requests.get(url)
    jsondata = r.json()
    items=[]
    for i in jsondata:
        if i=='153':
            _jsondata=jsondata[i]
            for j in _jsondata:
                items.append({
                    'label': j,
                    'thumbnail':j,
                    'path': j
                }) 


    return items

print get_tag_category()