import pymysql
con=pymysql.connect(**{
        'db': 'backend',
        'user': 'root',
        'password': 'dbpassword',
        'host': 'tongchengbin.cn'
})
cur=con.cursor()
import requests
while True:
    cur.execute('''select id,video_url from welfare_sexx where video_url not  like "%goovvg%" limit 10 ''')
    tasks=cur.fetchall()
    sql = """update welfare_sexx set video_url="%s" where id="%s" """
    params=[]
    for task in tasks:
        new_url=requests.head(task[1]).headers.get('Location')
        print(new_url)
        params.append([new_url,task[0]])
    cur.executemany(sql,params)
    con.commit()