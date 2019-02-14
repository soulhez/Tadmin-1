database_conf = {
        'host': '192.168.178.133',
        'user': 'root',
        'password': 'root',
        'db': 'backend',
        'charset': 'utf8'
}

import re
import requests
import datetime
import json

proxies = {'http': 'socks5://127.0.0.1:5001','https':'socks5://127.0.0.1:5001'}
def get_access_code(url):
    if re.findall(r'surl=(.+)', url):
        surl = re.findall(r'surl=(.+)', url)[0]
    elif url.startswith("https://pan.baidu.com/s/1"):
        surl = url.split("/")[-1][1:]
    else:
        print("没有匹配到参数")
        return {}
    print(surl)
    url = "https://ypsuperkey.meek.com.cn/api/items/BDY-%s?access_key=4fxNbkKKJX2pAm3b8AEu2zT5d2MbqGbD&client_version=2018.8" % surl
    r = requests.get(url,proxies=proxies)
    print(r.json())
    return r.json()


def collect_res():
    from bs4 import BeautifulSoup
    # 采集商品资源
    import pymysql
    con = pymysql.connect(**database_conf)
    cur = con.cursor(pymysql.cursors.DictCursor)
    from urllib import parse
    sql = 'select * from shop_goods where id>=190 order by id'
    cur.execute(sql)
    collected_sql=[]
    try:
        for record in cur.fetchall():
            temp_sql = []
            url = "https://www.yunpanjingling.com/search/%s" % (parse.quote(record['title']))
            r = requests.get(url, proxies=proxies)
            items = BeautifulSoup(r.text, 'html.parser').find_all(class_='item')
            for item in items[:10]:
                title = item.find(class_='name').get_text().strip()
                share_time = item.find(class_='share-time').get_text().strip()
                size = item.find(class_='size').get_text().strip()
                code_page = item.find(class_='code')
                code = code_page.text.strip() if code_page else ''
                refer_jump = item.find(class_='referrer').a.attrs['href']
                if refer_jump == 'https://noreferrer.meek.com.cn/redirect/':
                    refer = ''
                else:
                    jump_res = requests.get(refer_jump, proxies=proxies)
                    refer = re.search(r'url=(.+)"', jump_res.text).group(1)
                jump_url = item.find(class_='name').a.attrs['href']
                jump_res = requests.get(jump_url, proxies=proxies)
                pan_url = re.search(r'url=(.+)"', jump_res.text).group(1)
                # write sql to text
                sql = '''insert into shop_res(url,source,code,goods_id,`size`,title,col_time,share_time)\
                          values('{url}','{source}','{code}',{goods_id},'{size}','{title}','{col_time}','{share_time}') '''.format(
                    url=pan_url, source=refer, code=code, goods_id=record['id'],size=size ,title=title,
                    col_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), share_time=share_time)
                print(sql)
                temp_sql.append(sql)
            for sql in temp_sql:
                cur.execute(sql)
            con.commit()
    except Exception as e:
        print(e)
        print('ERROR=====================CURRENT ID ',record['id'])
    finally:
        print(record['id'])




