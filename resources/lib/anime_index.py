# -*- coding: utf-8 -*-
import urllib2, urllib, re, string, sys, os, gzip, StringIO
import math, os.path, httplib, time
import cookielib
import base64
from urllib import urlopen
import zlib
import urllib2
import zlib
import gzip
from io import BytesIO

UserAgent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

def getUrlResponse(url, postDict={}, headerDict={}, timeout=0, useGzip=False) :
    # makesure url is string, not unicode, otherwise urllib2.urlopen will error
    url = str(url);

    if (postDict) :
        postData = urllib.urlencode(postDict);
        req = urllib2.Request(url, postData);
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
    else :
        req = urllib2.Request(url);

    if(headerDict) :
        #print "added header:",headerDict;
        for key in headerDict.keys() :
            req.add_header(key, headerDict[key]);

    defHeaderDict = {
        'User-Agent'    : UserAgent,
        'Cache-Control' : 'no-cache',
        'Accept'        : '*/*',
        'Connection'    : 'Keep-Alive',
    };

    # add default headers firstly
    for eachDefHd in defHeaderDict.keys() :
        #print "add default header: %s=%s"%(eachDefHd,defHeaderDict[eachDefHd]);
        req.add_header(eachDefHd, defHeaderDict[eachDefHd]);

    if(useGzip) :
        #print "use gzip for",url;
        req.add_header('Accept-Encoding', 'gzip, deflate');

    # add customized header later -> allow overwrite default header 
    if(headerDict) :
        #print "added header:",headerDict;
        for key in headerDict.keys() :
            req.add_header(key, headerDict[key]);

    if(timeout > 0) :
        # set timeout value if necessary
        resp = urllib2.urlopen(req, timeout=timeout);
    else :
        resp = urllib2.urlopen(req);
    
    return resp;

def getUrlRespHtml(url, postDict={}, headerDict={}, timeout=0, useGzip=True) :
    resp = getUrlResponse(url, postDict, headerDict, timeout, useGzip);
    respHtml = resp.read();
    if(useGzip) :
        respInfo = resp.info();
        if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")) :
            respHtml = zlib.decompress(respHtml, 16+zlib.MAX_WBITS);

    return respHtml;

def _get_gzip_content(content):
    bytes_buffer = BytesIO(content)
    return gzip.GzipFile(fileobj=bytes_buffer).read()

def _get_zlib_content(content):
    page_content = zlib.decompress(content)
    return page_content


def get_page_content(page_full_url):
    try:
        response = urllib2.urlopen(page_full_url)
        if response.headers.get('content-encoding', '') == 'gzip':
            return _get_gzip_content(response.read())
        elif response.headers.get('content-encoding', '') == 'deflate':
            return _get_zlib_content(response.read())
        else:
            return response.read()
    except:
        return ''

#url=urllib.urlencode({'kw':'http://www.bilibili.com/video/av2119723/'})
p_url='http://www.bilibili.com/list/b--a--t----d---1.html'
html = get_page_content(p_url)

html = html.replace('\r', '')
html = html.replace('\n', '')

anime = re.compile('<ul class="v_ul">(.+?)</ul>').findall(html)



if len(anime):
    anime = anime[0].replace('\r', '')
    anime = anime.replace('\n', '')
    anime = re.compile('<li>(.+?)</li>').findall(anime)


    for _anime in anime:
        #print _anime
        #_anime=_anime.replace(' ', '')
        #print _anime
        
        cover = re.compile('<div class="cover">(.+?)</div>').findall(_anime)
        info_wrp = re.compile('<div class="info_wrp">(.+?)</div>').findall(_anime)
        info_series = re.compile('<p class="num">(.+?)</p>').findall(_anime)
        



        image=""
        link=""
        title=""

        if len(cover):
            _cover = re.compile('<a href="/sp/(.+?)" target="_blank"><img src="(.+?)" /></a>').findall(cover[0])
            if len(_cover):
                image = _cover[0][1]
                link = _cover[0][0]

        if len(info_wrp):
            _info_wrp = re.compile('<a title="(.+?)" href="/sp/(.+?)" target="_blank">(.+?)</a>').findall(info_wrp[0])

            if len(_info_wrp):
                title=_info_wrp[0][0]

        if len(info_series):
            info_series=info_series[0].replace('<b>', '')
            info_series=info_series.replace('</b>', '')
            title=title+"  "+info_series

        print title
        break


    #links = re.compile('<a href="/video/(.+?)/" title="(.+?)" target="_blank">(.+?)</a>').findall(anime[0])


#if len(anime):
#    links = re.compile('<a href="/video/(.+?)/" title="(.+?)" target="_blank">(.+?)</a>').findall(anime[0])
#    #
#
#    for p in links:
#        print (p[0])
#        print (p[1])
#        img = re.compile('<img src="(.+?)"').findall(p[2])
#        #print (p[2])
#        print img[0]
#'''
    

#print attrs
#http://www.bilibili.com/video/av2137301/