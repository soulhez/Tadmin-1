import requests
from bs4 import BeautifulSoup
import re
import threading
import pymysql
config = {
    'host': 'tongchengbin.cn',
    'user': 'root',
    'password': 'dbpassword',
    'db': 'backend',
    'charset': 'utf8'
}
conn = pymysql.connect(**config)
cur = conn.cursor(pymysql.cursors.DictCursor)
req = requests.session()
req.headers = {
    'Host': 'www.kdw018.com',
    'Content-Type':'application/xml',
    "Connection": "keep-alive",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

res=req.get('http://www.kdw018.com/')
def date_parser(sdate):
    import datetime
    now = datetime.datetime.now()
    if '小时' in sdate:
        delta = datetime.timedelta(hours=int(sdate.strip("小时前")))
    elif '天' in sdate:
        delta = datetime.timedelta(days=int(sdate.strip("天前")))
    elif '月' in sdate:
        delta = datetime.timedelta(days=int(sdate.strip("月前")) * 30)
    elif '年' in sdate:
        delta = datetime.timedelta(days=int(sdate.strip("年前")) * 365)
    else:
        return now.strftime('%Y-%m-%d %H:%M:%S')
    n_days = now - delta
    return n_days.strftime('%Y-%m-%d %H:%M:%S')




def get_url():
    '''
      获取所有资源url
    '''

    flag = 1
    page = 1
    items_url = []
    while flag:
        page_url = 'http://www.kdw001.com/?mode=async&function=get_block&block_id=list_videos_most_recent_videos&sort_by=post_date&from={page}'.format(page=page)
        resp = req.get(page_url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text,'html.parser')
            items_title =[]
            for tag in soup.find_all(class_='item'):
                items_title.append(tag.find(class_='title').text.strip())
                items_url.append(tag.a.attrs['href'])
            # 查询数据库 如果有记录 不翻页 如果没有记录 翻页继续
            cur.execute('''select count(*) as cnt from  welfare_sexx where title in %s ''' % str(tuple(items_title)))
            cnt = cur.fetchone()
            if cnt['cnt'] >2:
                flag = 0
            #获取url 中的信息
            page +=1
    # item_url 本次任务
    return items_url




def get_info(items_url):
    '''
     获取详细信息
    '''
    while True:
        try:
            url = items_url.pop()
            print(url)
        except:
            break
        try:
            resp = requests.get(url)
        except BaseException:
            continue
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.find('h1').text.replace("'", "\\'")
            try:
                videoid = soup.find(
                    attrs={'href': '#like'}).attrs['data-video-id']
            except BaseException:
                print(url)
                continue
            upload_time_temp = soup.select('.info .item')[0].find_all('span')[
                2].text.split(":")[1].strip()
            video_time = soup.select('.info .item')[0].find_all('span')[
                0].text.replace('时长: ', '')
            views_num = soup.select('.info .item')[0].find_all('span')[
                1].find('em').text.replace(' ', '')
            vate_num = soup.find(
                class_='scale-holder').span.attrs['data-votes']
            praise_rate = soup.find(
                class_='scale-holder').span.attrs['style'].split(':')[1].strip('%;')
            summary = ''
            tags = ''
            classes = ''
            for item in soup.select('.info .item'):
                if "描述:" in item.text:
                    summary = item.find('em').get_text()
                if "标签:" in item.text:
                    tags = ','.join([i.text for i in soup.select(
                        '.info .item')[3].find_all('a')])
                if "类别::" in item.text:
                    classes = ','.join(
                        [i.text for i in soup.select('.info .item')[2].find_all('a')])
            video_url = soup.select('.info .item')[-1].find('a').attrs['href']
            video_size = soup.select('.info .item')[-1].find('a').text
            video_img = soup.find(
                attrs={
                    'property': 'og:image'}).attrs['content'].replace(
                '.mp4',
                '').replace(
                ' ',
                '')
            index_img = video_img.replace(
                'preview.mp4.jpg', '180x135/1.jpg').replace(' ', '')
            # 插入数据
            sql = '''
                insert into welfare_sexx(videoid,title,url,upload_time,index_img,vote_num,praise_rate,
                video_time,views_num,summary,classes,tags,video_img,video_size,video_url,ctime)
                values({videoid},'{title}','{url}','{upload_time}','{index_img}',{vote_num},'{praise_rate}',
                '{video_time}',{views_num},'{summary}','{classes}','{tags}','{video_img}','{video_size}','{video_url}',now())
                '''.format(videoid=videoid,
                           title=title,
                           url=url,
                           upload_time=date_parser(upload_time_temp),
                           index_img=index_img,
                           vote_num=vate_num,
                           praise_rate=praise_rate,
                           video_time=video_time,
                           views_num=views_num,
                           summary=summary,
                           classes=classes,
                           tags=tags,
                           video_img=video_img,
                           video_size=video_size,
                           video_url=video_url)
            try:
                cur.execute(sql)
                conn.commit()
            except Exception as e:
                print(sql)

if __name__ == "__main__":
    item_url = get_url()
    get_info(item_url)


