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
p_url='http://www.bilibili.com/video/music-coordinate-1.html'
html = get_page_content(p_url)
 
print html



attrs = re.compile('<div class="l-item"><a href="/video/(.+?)/" target="_blank" class="preview"><img src="(.+?)"></a><a href="/video/(.+?)/" target="_blank" class="title">(.+?)</a>').findall(html)

x= [{
    'title': i[3],
    'link': 'http://cn-jsyz2-dx.acgvideo.com/vg3/c/7c/3252803-1.flv?expires=1426653000&ssig=-aqPxK4IjjdgL5M25DupPQ&o=2095617680&rate=0',
    'description': i[3],
    'thumbnail':i[1],
    'published': i[0]} for i in attrs]

for i in (x):
    print i['title']


#print attrs