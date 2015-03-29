#coding: utf8

from config import *
import feedparser
import xml.dom.minidom as minidom
import re
import time
import datetime
import os
import tempfile
import utils
import cPickle as pickle
from niconvert import create_website
import json

import urllib2, urllib, string, sys,  gzip, StringIO
import math, os.path, httplib
import cookielib
import base64
from urllib import urlopen


UserAgent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

class Bili():
    def __init__(self, width=720, height=480):
        self.WIDTH = width                                          # 屏幕宽度，用于确定弹幕大小
        self.HEIGHT = height                                        # 屏幕高度，用于确定弹幕大小
        self.BASE_URL = BASE_URL                                    # B站根地址
        self.RSS_URLS = RSS_URLS                                    # B站RSS地址
        self.INDEX_URLS = INDEX_URLS                                # B站索引地址
        self.ROOT_PATH = ROOT_PATH                                  # 根菜单
        self.CAT_URLS = CAT_URLS                                  
        self.HOT_CATS = HOT_CATS                                  
        self.LIST_TYPE = LIST_TYPE                                  # 列表类型
        self.INTERFACE_URL = INTERFACE_URL                          # 视频地址请求页面地址
        self.COMMENT_URL = COMMENT_URL                              # 评论页面地址
        self.URL_PARAMS = re.compile('cid=(\d+)&(?:bili-)?aid=\d+')           # 匹配视频请求ID(cid)
        self.URL_PARAMS2 = re.compile("cid:'(\d+)'")                # 匹配另一种页面上的视频请求ID(cid)
        # 匹配视频列表
        self.PARTS = re.compile("<option value=.{1}(/video/av\d+/index_\d+\.html).*>(.*)</option>")
        # 匹配索引视频列表
        self.ITEMS = re.compile('<li.*?pubdate="(.*?)">.*?<a href=".*?av(\d+)/".*?>(.*?)</a></li>')
        # 生成完整的URL
        for item in self.RSS_URLS:
            item['url'] = self.BASE_URL + item['url']
        for item in self.INDEX_URLS:
            item['url'] = self.BASE_URL + item['url']
        try:
            os.remove(self._get_tmp_dir() + '/tmp.ass')
        except:
            pass

    def _get_tmp_dir(self):
        if len(TEMP_DIR) != 0:
            return TEMP_DIR
        try:
            return tempfile.gettempdir()
        except:
            return TEMP_DIR

    def _print_info(self, info):
        print '[Bilibili]: ' + info

    # 根据英文名称返回URL
    def _get_url(self, dict_obj, name):
        for item in dict_obj:
            if item['eng_name'] == name:
                return item['url']
            else:
                return 'video/'+name

    # 根据英文名称获取RSS页面URL
    def _get_rss_url(self, name):
        return self._get_url(self.RSS_URLS, name)

    # 根据英文名称获取索引页面URL
    def _get_cat_url(self, name):
        return self.BASE_URL+self._get_url(self.CAT_URLS, name)

    def _get_index_url(self, name):
        return self._get_url(self.INDEX_URLS, name)

    # 根据页面内容解析视频请求页面URL
    def _parse_urls(self, page_content, need_subtitle = True):
        self._print_info('Parsing page')
        url_params = self.URL_PARAMS.findall(page_content)
        interface_full_url = ''
        # 如果使用第一种正则匹配成功
        if url_params and len(url_params) == 1 and url_params[0]:
            interface_full_url = self.INTERFACE_URL.format(str(url_params[0]))
        # 如果匹配不成功则使用第二种正则匹配
        if not url_params:
            self._print_info('Parsing page by another regex')
            url_params = self.URL_PARAMS2.findall(page_content)
            if url_params and len(url_params) == 1 and url_params[0]:
                interface_full_url = self.INTERFACE_URL.format(str(url_params[0]))
        if interface_full_url:
            self._print_info('Interface url: ' + interface_full_url)
            # 解析RSS页面
            self._print_info('Getting video address by interface page')
            content = utils.get_page_content(interface_full_url)
            self._print_info('Interface page length: ' + str(len(content)))
            doc = minidom.parseString(content)
            parts = doc.getElementsByTagName('durl')
            self._print_info('Video parts found: ' + str(len(parts)))
            result = []
            # 找出所有视频地址
            for part in parts:
                urls = part.getElementsByTagName('url')
                if len(urls) > 0:
                    result.append(urls[0].firstChild.nodeValue)
            if need_subtitle:
                return (result, self._parse_subtitle(url_params[0]))
            else:
                return (result, '')
        else:
            self._print_info('Interface url not found!')
        return ([], '')

    # 调用niconvert生成弹幕的ass文件
    def _parse_subtitle(self, cid):
        page_full_url = self.COMMENT_URL.format(cid)
        self._print_info('Page full url: ' + page_full_url)
        website = None
        try:
            website = create_website(page_full_url)
            if website is None:
                self._print_info(page_full_url + " not supported")
                return ''
            else:
                self._print_info('Generating subtitle')
                text = website.ass_subtitles_text(
                    font_name=u'黑体',
                    font_size=36,
                    resolution='%d:%d' % (self.WIDTH, self.HEIGHT),
                    line_count=12,
                    bottom_margin=0,
                    tune_seconds=0
                )
                f = open(self._get_tmp_dir() + '/tmp.ass', 'w')
                f.write(text.encode('utf8'))
                f.close()
                self._print_info('Subtitle generation succeeded!')
                return 'tmp.ass'
        except Exception as e:
            self._print_info("Exception raised when generating subtitle: %s" % e)
            return ''

    def _need_rebuild(self, file_path):
        return time.localtime(os.stat(file_path).st_ctime).tm_mday != time.localtime().tm_mday

    def _get_index_items_from_web(self, url):
        page_content = utils.get_page_content(url)
        results_dict = dict()
        results_month_dict = dict()
        parts = page_content.split('<h3>')
        for part in parts:
            results = self.ITEMS.findall(part)
            key = part[0]
            results_dict[key] = []
            for r in results:
                results_dict[key].append((r[1], r[2], r[0]))
                if r[0] in results_month_dict.keys():
                    results_month_dict[r[0]].append((r[1], r[2]))
                else:
                    results_month_dict[r[0]] = [(r[1], r[2])]
        return results_dict, results_month_dict

    # 获取索引项目，并缓存
    def _get_index_items(self, url):
        pickle_file_by_word = self._get_tmp_dir() + '/' + url.split('/')[-1].strip() + '_word_tmp.pickle'
        pickle_file_by_month = self._get_tmp_dir() + '/' + url.split('/')[-1].strip() + '_month_tmp.pickle'
        try:
            if  os.path.exists(pickle_file_by_word) and os.path.exists(pickle_file_by_month) and not self._need_rebuild(pickle_file_by_word) and not self._need_rebuild(pickle_file_by_month):
                self._print_info('Index files already exists!')
                return pickle.load(open(pickle_file_by_word, 'rb')), pickle.load(open(pickle_file_by_month, 'rb'))
            else:
                results_dict, results_month_dict = self._get_index_items_from_web(url)
                try:
                    word_file = open(pickle_file_by_word, 'wb')
                    month_file = open(pickle_file_by_month, 'wb')
                    pickle.dump(results_dict, word_file)
                    pickle.dump(results_month_dict, month_file)
                    self._print_info('Index files fetched succeeded!')
                except:
                    self._print_info('Index files generate failed!')
                return results_dict, results_month_dict
        except:
            return self._get_index_items_from_web(url)

 

    # 获取RSS项目，返回合法的菜单列表
    def get_rss_items(self, category):
        self._print_info('Getting RSS Items')
        rss_url = self._get_rss_url(category)
        parse_result = feedparser.parse(rss_url)
        self._print_info('RSS Items fetched succeeded!')
        return [ {
            'title': x.title,
            'link': x.link.replace(BASE_URL+'video/av', '').replace('/', ''),
            'description': x.description,
            'published': x.published
        } for x in parse_result.entries ]

    # 获取索引项目，返回合法的菜单列表
    def get_index_items(self, category, type_id=0):
        self._print_info('Getting Index Items')
        if type_id > 1:
            return []
        index_url = self._get_index_url(category)
        parse_result = self._get_index_items(index_url)
        self._print_info('Index items fetched succeeded!')
        return [ {
            'title': x,
            'link': x,
            'description': x,
            'published': x
        } for x in sorted(parse_result[type_id].keys(), reverse=bool(type_id))]



    def get_hotjson_items(self,type, category):
        self._print_info('Getting HOT CAT JSON Items')
        self._print_info(category)
        json_url = 'http://www.bilibili.com/index/rank/all-1-3.json'
        self._print_info(json_url) 
        self._print_info('HOT CAT Items fetched succeeded!')
 
        html= utils.get_page_content(json_url)


        data=json.loads(html)
        data=(data['rank']['list'])


        temp=[]

    

        for i in range(0,len(data)):
            #pprint(data[i])
            aid= 'av'+str(data[i]['aid'])
            title=(data[i]['title'])
            author=(data[i]['author'])
            description=(data[i]['description'])
            mid=(data[i]['mid'])
            pic=(data[i]['pic'])
            link= 'http://www.bilibili.com/video/'+str(aid)

            temp.append({
            'title': title,
            'link': link,
            'category':category,
            'description':description,
            'thumbnail':pic,
            'published': aid })


            #temp.append({
            #    'title': title,
            #    'link': 'http://www.bilibili.com/video/av'+aid,
            #    'category':category,
            #    'description':description,
            #    'thumbnail':pic,
            #    'published': 'av'+aid })



        return temp



    def get_hot_items(self, category):
        self._print_info('Getting HOT CAT Items')
        self._print_info(category)
        cat_url = self._get_cat_url(category)
        self._print_info(cat_url)
        #parse_result = feedparser.parse(cat_url)
        self._print_info('HOT CAT Items fetched succeeded!')
 
        html= utils.get_page_content(cat_url)


        temp=[]
        pager = re.compile('<ul class="rlist">(.+?)</ul>').findall(html)

        if len(pager):
            links = re.compile('<a href="/video/(.+?)/" title="(.+?)" target="_blank">(.+?)</a>').findall(pager[0])
            

            for p in links:
                img = re.compile('<img src="(.+?)"').findall(p[2])
                temp.append({
                    'title': p[1],
                    'link': p[0],
                    'category':category,
                    'description': p[0],
                    'thumbnail':img[0],
                    'published': p[0]})



        return temp

    def get_cat_items(self, category):
        self._print_info('Getting CAT Items')
        self._print_info(category)
        cat_url = self._get_cat_url(category)
        self._print_info(cat_url)
        #parse_result = feedparser.parse(cat_url)
        self._print_info('CAT Items fetched succeeded!')
 
        html= utils.get_page_content(cat_url)
        attrs = re.compile('<div class="l-item"><a href="/video/(.+?)/" target="_blank" class="preview"><img src="(.+?)"></a><a href="/video/(.+?)/" target="_blank" class="title">(.+?)</a>').findall(html)
        
        temp= [{
            'title': i[3],
            'description': i[3],
            'link':'',
            'category':category,
            'thumbnail':i[1],
            'published': i[0]} for i in attrs]

        #for t in temp:
        #    for tt in t:
        #        self._print_info(t[tt])



        pager = re.compile('<div class="pagelistbox">(.+?)</div>').findall(html)

        if len(pager):
            links = re.compile('href="/video/(.+?)">(.+?)</a>').findall(pager[0])


            for p in links:
                if p[1] == '下页' or p[1] == '末页' or p[1] == '首页 ' or p[1] == '上页 ':
                    temp.append({
                        'title': p[1],
                        'link': p[0],
                        'category':p[0],
                        'description': p[1],
                        'thumbnail':p[1],
                        'published': p[0]})
                else:
                    temp.append({
                        'title': '第'+p[1]+'页',
                        'link': p[0],
                        'category':p[0],
                        'description': p[1],
                        'thumbnail':p[1],
                        'published': p[0]})

        return temp



    def get_video_paths(self,category,video):
        self._print_info('Getting Video Urls')
  



        video_urls=[]


        title=video
        description=video
        thumbnail=video
        id=video

        p_url='http://www.bilibili.com/video/'+id
        html = utils.get_page_content(p_url)


        self._print_info(p_url)
        self._print_info('Video url fetched succeeded!')


        attrs = re.compile("<option value='(.+?)'>(.+?)</option>").findall(html)

        parts =False

        for i in attrs:
            parts=True
            video_urls.append({
                'title': i[1],
                'link': i[0],
                'part': i[0],
                'category':category,
                'description': i[1],
                'thumbnail':i[1],
                'published': id})


        if parts:
            self._print_info('has parts')
        else:


            self._print_info('no  parts')


        self._print_info('End of fetch')
        return video_urls


    def get_video_parts(self,category,video,part):
        self._print_info('Getting Video Parts')
        self._print_info(video)
        #parse_result = feedparser.parse(cat_url)
        self._print_info('Parts fetched succeeded!')
  



        video_urls=[]


        title=part
        description=part
        thumbnail=video
        id=video


        url=urllib.urlencode({'kw':'http://www.bilibili.com/video/'+id})
       

        p_url='http://www.flvcd.com/parse.php?format=&'+url
        html2 = utils.get_page_content(p_url)
        html2=html2.decode('gbk').encode('utf-8')
        

        attrs2 = re.compile('<input type="hidden" name="(.+?)" value="(.*?)"').findall(html2)




        filename=""
        inf=""
        for i in (attrs2):
            if i[0]=="filename":
                filename=i[1]
            if i[0]=="inf":
                inf=i[1]

        link=inf

                

        video_urls.append({
            'title': '播放',
            'link': link,
            'category':category,
            'description': description,
            'thumbnail':thumbnail,
            'published': id})

        return video_urls


    # 从缓存字典中返回视频结果
    def get_video_by_ident(self, category, display_type, ident):
        self._print_info('Getting items from cache')
        index_url = self._get_index_url(category)
        parse_result = self._get_index_items(index_url)
        self._print_info('Cached items fetched succeeded!')
        return [ {
            'title': x[1],
            'link': x[0],
            'description': x[1],
            'published': ident
        } for x in parse_result[display_type][ident] ]

    # 根据不同类型返回相应的视频列表
    def get_items(self, target, category=None):
        self._print_info('Getting items by type')
        if category:
            return self.get_cat_items(category)
        else:
            return self.CAT_URLS
 


    # 获取一个页面的所有视频
    def get_video_list(self, av_id):
        page_full_url = self.BASE_URL + 'video/av' + str(av_id) + '/'
        page_content = utils.get_page_content(page_full_url)
        parts = self.PARTS.findall(page_content)
        if len(parts) == 0:
            return [(u'播放', 'video/av' + str(av_id) + '/')]
        else:
            return [(part[1], part[0][1:]) for part in parts]

    # 获取视频地址
    def get_video_urls(self, url, need_subtitle=True):
        self._print_info('Getting video address')
        page_full_url = self.BASE_URL + url
        self._print_info('Page url: ' + page_full_url)
        page_content = utils.get_page_content(page_full_url)
        self._print_info('Origin page length: ' + str(len(page_content)))
        return self._parse_urls(page_content, need_subtitle)
