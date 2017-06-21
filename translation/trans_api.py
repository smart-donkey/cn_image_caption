#/usr/bin/env python
#coding=utf8
 
import httplib
import urllib2
import random
import json
import md5

appid = '20160715000025271'
secretKey = 'NZBmOnjrNLDxThhrJEUA'

def translation_en_zh(q):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    # q = 'A group of people sitting about table eat something.'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib2.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        req = urllib2.Request('http://api.fanyi.baidu.com' + myurl)
        response = urllib2.urlopen(req)
        the_page = response.read()
        json_data = json.loads(the_page)
        return (json_data["trans_result"][0]["dst"])

        #response是HTTPResponse对象
    except Exception, e:
        print e
