import json
import time
import requests
import base64
import execjs
import io
import cv2
import os
import numpy as np
from PIL import Image
import math
import random
import re

os.environ["EXECJS_RUNTIME"] = "PhantomJS"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}


down = lambda x:[[x,32+i] for i in range(0,97,3)] #竖向轨迹列表
right = lambda y:[[32+i,y]for i in range(0,97,3)] #横向轨迹列表
r_d = [[32+i,32+i] for i in range(0,97,3)]  #右下轨迹
r_u = [[32+i,128-i] for i in range(0,97,3)] #右上轨迹


def login(username,pwd):
    s = requests.session()
    s.get("   ",headers=headers)#获取cookie
    while 1:
        url = 'https://login.sina.com.cn/sso/prelogin.php?checkpin=1&entry=mweibo&su=MTgzOTc1Njg0ODE=&callback=jsonpcallback1525741684767'
        # https://login.sina.com.cn/sso/prelogin.php?checkpin=1&entry=mweibo&su=b'MTgzOTc1Njg0ODE='&callback=jsonpcallback1525741674860
        url = 'https://login.sina.com.cn/sso/prelogin.php?checkpin=1&entry=mweibo&su=%s&callback=jsonpcallback%s' % (
        base64.b64encode(username.encode('utf-8')).decode('utf-8'), int(time.time() * 1000))
        data = s.get(url, headers=headers)
        data=eval(re.search(r"\((.+)\)",data.text).group(1))
        #如果data.get('showpin')等于1 ，需要输入验证码
        if data.get('showpin') == 1:
            data = {'ver': 'daf139fb2696a4540b298756bd06266a',
                    'source': 'ssologin',
                    'usrname': username,
                    'line': 160,
                    'side': 100,
                    'radius': '30',
                    '_rnd': '0.07298144508429671',
                    'callback': 'pl_cb'}
            #获取base64编码的图片
            data = s.get('https://captcha.weibo.com/api/pattern/get', params=data).content[6:-1]
            data = json.loads(data)
            path_enc = data['path_enc']
            vid = data['id']
            #解析图片并生成轨迹
            data_enc, path_enc = decodeimg(path_enc,vid)
            if data_enc==0:
                continue
            data = {
                'ver': 'daf139fb2696a4540b298756bd06266a',
                'id': vid,
                'usrname': username,
                'source': 'ssologin',
                'path_enc': path_enc,
                'data_enc':data_enc,
                'callback': 'pl_cb'
            }
            data = s.get('https://captcha.weibo.com/api/pattern/verify',params=data)
            data=data.text
            # print(json.loads(data[6:-1])['msg'])
            if json.loads(data[6:-1])['code']=="100000":
                break
        else:
            vid=''
            break

    data='username={}&password={}&savestate=1&r=http%3A%2F%2Fweibo.cn%2F&ec=0&pagerefer=&entry=mweibo&wentry=&loginfrom=&client_id=&code=&qq=&mainpageflag=1&vid={}&hff=&hfp='.format(username,pwd,vid)
    headers['Referer']="https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt="
    headers['Content-Type']="application/x-www-form-urlencoded"
    a = s.post('https://passport.weibo.cn/sso/login',headers=headers,data=data).json()
    if a['retcode']==20000000:
        s.get(a['data']['crossdomainlist']['weibo.com'],headers=headers)
        # res = s.get('http://weibo.com')
        # res = s.get('http://www.weibo.com/237506788')
        # page = s.get('http://weibo.cn').content
        # tree = etree.HTML(page)
        # a  = tree.xpath("//div[@class='ut']/text()")[0]
        print('登录成功')
        return s
    else:
        if a['retcode']==50011005:
            return 0
def check(l):
    l1=[]
    if not len(l):return []
    if isinstance(l[0],tuple) and len(l)>=2:
        n=0
        for i in l[:-1]:
            n+=1
            for j in l[n:]:
                if checkr(i,j):
                    l1.append(j)
        for i in l1:
            try:
                l.remove(i)
            except:
                pass
    return l
def checkr(a,b):
    if math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)<30:
        return True
def join(a,b):
    #连接线条
    if a[0]==b[-1]:
        return b+a
    if a[-1]==b[0]:
        return a+b
def remove(l):
    # 模板匹配不精确，移除不和其他线条相连的线条
    if len(l)>3:
        for i in l:
            for j in l:
                if (i[0]==j[-1] or i[-1]==j[0]) and not (i[0]==j[-1] and i[-1]==j[0]):
                    break
            else:

                l.remove(i)
        return l
    else:
        return l
def getpath(l):
    #获取线条其实位置index
    p=['1','2','3','4']
    d=[]

    for i in (l[0],l[33],l[66]):
        if i[:2]==[32,32]:
            p.remove('1')
            d.append('1')
        if i[:2]==[128,32]:
            p.remove('2')
            d.append('2')
        if i[:2]==[32,128]:
            p.remove('3')
            d.append('3')
        if i[:2]==[128,128]:
            p.remove('4')
            d.append('4')
    d.extend(p)
    return ''.join(d)

def decodeimg(path_enc=None,id=None):
    path_enc, path_l = path_enc.replace("data:image/gif;base64,", "").split("|")
    #还原图片
    imgdata = base64.b64decode(path_enc)
    js = open('decode.js').read()
    js = execjs.compile(js)
    indexlist = js.call('getimgpx', path_l)
    # print(js._runtime.name)
    indexlist = [(_.split(' ')[0], _.split(' ')[1]) for _ in indexlist.split(";") if _]
    image = Image.open(io.BytesIO(imgdata))
    #获取真实图片
    image = get_img(image, indexlist)
    time.sleep(1)#等待；不然会报请求频繁
    image.save('code.png')
    l=[] #存储所有匹配到的箭头产生的轨迹
    for each in os.listdir('./flag'):
        for i in mathc_img('code.png','./flag/%s'%each):#匹配各种箭头
            if len(i):
                types =  each.split('.')[0]
                if types in ['l','r']:
                    y = [128  if abs(_[1]-128)<20 else 32 for _ in i] if isinstance(i[0],tuple)>1 else ( 128  if abs(i[1]-128)<20 else 32 ),#标准化每个线条起始点，方便识别顺序
                    if types=='l':
                        for i in y:
                            li = right(i)
                            li.reverse()#根据决定性坐标判断线条位置
                            l.append(li)
                    else:
                        for i in y:
                            li = right(i)
                            l.append(li)
                elif types in ['u','d']:
                    x = set([128  if abs(_[0]-128)<20 else 32 for _ in i]) if isinstance(i[0], tuple) > 1 else ( 128  if abs(i[0]-128)<20 else 32 ),#标准化每个线条起始点，方便识别顺序
                    if types=='u':
                        for i in x:
                            li = down(i)
                            li.reverse()
                            l.append(li)
                    else:
                        for i in x:
                            li = down(i)
                            l.append(li)
                else:
                    if types in ['r_d','l_u']:
                        li = r_d
                        if types == 'l_u':
                            if not checkr(i,(91, 90)):li=[]
                            li.reverse()
                        if types == 'r_d':
                            if not checkr(i,(54, 49)):li=[]
                        l.append(li)
                    if types in ['r_u','l_d']:
                        li = r_u
                        if types == 'l_d':
                            if not checkr(i, (92, 48)): li = []
                            li.reverse()
                        else:
                            if not checkr(i, (52, 93)): li = []
                        l.append(li)
    try:
        l=remove(l)
    except:
        return 0,0
    if len(l)!=3:return 0,0 #不是3个线条的 重来
    l1 = join(l[0],l[1])
    if l1:
        l = join(l1,l[2])
    else:
        l1 = join(l[0],l[2])
        if l1:
            l = join(l1,l[1])
        else:
            return 0,0
    try:
        l = [l[i]+[int(time.time()*1000)] if i==0 else l[i]+[i*10+random.randint(0,5)]  for i in range(len(l))]
        path_enc = getpath(l)
    except:
        return 0,0
    js = open('decode.js').read()
    js = execjs.compile(js)
    l = json.dumps(l)
    path_enc=path_enc.replace("\/","/")
    data_enc = js.call('encode', l) #编码data_enc
    path_enc = js.call('pencode', path_enc+"%%"+id)#编码path_enc
    return data_enc,path_enc

def get_img(image, indexlist):
    #拼接真是图片
    temp1 = Image.new('RGB', (160, 160))
    n = 0
    for each in indexlist:
        x = int(each[0])
        y = int(each[1])
        box = (x, y, x + 32, y + 32)
        temp = image.crop(box)
        y, x = divmod(n, 5)
        x, y = x * 32, y * 32
        n+=1
        temp1.paste(temp, (x, y, x + 32, y + 32))
    return temp1

def mathc_img(image,Target,value=0.93):
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target,0)
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where( res >= threshold)
    return check([pt for pt in zip(*loc[::-1])])


if __name__ == '__main__':
    login('18397568481','bbtgzn735')
