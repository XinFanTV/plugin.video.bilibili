# -*- coding: utf-8 -*-

import sys
import json,urllib
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


strx='剧场版'
print strx
print urllib.quote_plus(str(strx.encode("utf-8")))
#exit()

url="http://www.bilibili.com/index/tag/33/default/1/%E5%89%A7%E5%9C%BA%E7%89%88.json"
r = requests.get(url)
jsondata = r.json()
item=[]
for i in jsondata:
  _jsondata=jsondata[i]
  if type(_jsondata) is list:
    for j in _jsondata:
      #item[k]=j[k]
      for k in j:
        print k,j[k]
      print "\t"
      #print _jsondata[j]
      print "\n\n---"
      exit()
  else:
    print 'test'
    print i,_jsondata
  #for j in _jsondata:
  #  print j
    #print _jsondata[j]
    #print "\t"

  print "\n"

exit()

response = urllib.urlopen(url)
data = json.loads(response.read())
print data
