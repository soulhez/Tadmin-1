import requests
import redis
import time
import re
import threading
import random
import json
rd = redis.Redis(host='127.0.0.1',db=3)
import  pymysql
# config = {
#     'host':'127.0.0.1',
#     'user':'root',
#     'password':'root',
#     'db':'welfare',
#     'charset':'utf8'
# }
# data = rd.smembers('sexxurl')
# with open('data.json','a+') as f:
#     f.write(str(data))

f = open('data.json','r',encoding='utf-8').read()
for i in eval(f):
    rd.sadd('sexxurl',i.decode('utf-8'))