'''
项目初始化脚本   数据采集
'''
import sys,os
django_env = True
if django_env:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    import django  # 加载django
    django.setup()

import pymysql
databases = {
    'user':'root',
    'password':'dbpassword',
    'db':'backend',
    'host':'tongchengbin.cn',
    'port':3306
}

con = pymysql.connect(**databases)
cur = con.cursor(pymysql.cursors.DictCursor)
def invery_goods():
    '''
        慕课网视频采集
        clear table
    '''
    # cur.execute('''truncate shop_goods''')
    # con.commit()
    # cur.execute('''truncate shop_lang''')
    # con.commit()
    import requests
    from bs4 import BeautifulSoup
    url = 'https://coding.imooc.com'
    index = requests.get(url)
    index.encoding = 'utf-8'
    soup = BeautifulSoup(index.text, 'html.parser')
    for tag in soup.find_all(class_='shizhan-skill clearfix')[0].find_all('a')[1:]:
        en = tag.attrs['data-ct']
        cn =tag.text
        sql= ''' insert into shop_lang(en,cn) values('{}','{}') '''.format(en,cn)
        cur.execute(sql)
        con.commit()
        lang_id = '''select '''
        full_url = url + tag.attrs['href']
        second_page = requests.get(full_url)
        second_page.encoding = 'utf-8'
        second_soup = BeautifulSoup(second_page.text, 'html.parser')
        for box in second_soup.find_all(class_='box'):
            classurl = url+box.parent.parent.attrs['href']
            img = 'http://' + box.find_all('img')[0].attrs['src']
            title = box.find_all(class_='shizan-name')[0].attrs['title']
            desc = box.find_all(class_='shizan-desc')[0].attrs['title']
            price = box.find_all(class_='course-card-price')[0].text[1:]
            goods_sql = ''' insert into shop_goods(title,`desc`,price,default_img,lang_id,url) values('{}','{}',{},'{}',(select id from shop_lang where en='{}' limit 1),'{}')'''.format(
               title, desc, price, img,en,classurl)
            print(goods_sql)
            try:
                cur.execute(goods_sql)
                con.commit()
            except pymysql.err.IntegrityError:
                pass


def mooc_to_cursor():
    from shop.models import Course, imooc
    data = imooc.objects.all()
    querylist= []
    for obj in data:
        querylist.append(Course(title=obj.title,desc=obj.desc,content=obj.content,source_url=obj.url,source_name='慕课网',
                                res=obj.res,default_img=obj.default_img,tags=obj.lang.cn))
    Course.objects.bulk_create(querylist)
mooc_to_cursor()