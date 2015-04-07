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

 


def getNextpage(list,bangumi,page):
    p_url='http://www.bilibili.com/sppage/bangumi-'+str(bangumi)+'-'+str(page)+'.html'
    html = get_page_content(p_url)

    html = html.replace('\r', '')
    html = html.replace('\n', '')

    checknext = re.compile('<div class="no_more">(.+?)</div>').findall(html)
    if len(checknext):
        if checknext[0]=="没有更多信息":
            return list

    else:
        series = re.compile('<a class="t" href="(.+?)" target="_blank">(.+?)</a>').findall(html)

        if len(series):
            for s in series:
                list.append({
                    'title': s[1].strip(),
                    'link': s[0].strip(),
                    'type': 'bangumi',
                    'page': page,
                    'thumbnail':s[0].strip(),
                    'published': s[0].strip()})

        return getNextpage(list,bangumi,page+1)

list=[]


#print getNextpage(list,507,1)

url="http://www.bilibili.com/sp/%E9%BB%8F%E9%BB%8F%E7%B3%8A%E7%B3%8A%EF%BC%81%EF%BC%81%E8%A7%92%E8%B4%A8%E5%90%9B#S-1817"



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