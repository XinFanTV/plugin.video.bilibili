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
import json
from pprint import pprint



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



url="http://www.bilibili.com/index/rank/all-1-3.json"
html = get_page_content(url)
data=json.loads(html)
 

data=(data['rank']['list'])

#print len(data)




for i in range(0,len(data)):
    #pprint(data[i])
    aid=(data[i]['aid'])
    title=(data[i]['title'])
    author=(data[i]['author'])
    description=(data[i]['description'])
    mid=(data[i]['mid'])
    pic=(data[i]['pic'])
    print 'http://www.bilibili.com/video/'+str(aid)


#pprint(data)