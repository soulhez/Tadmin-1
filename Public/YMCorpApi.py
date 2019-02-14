# author:mr.tong
# date:2018/5/24
import json
import requests
import redis
import time
HOST = 'http://api.fxhyd.cn'
cache = redis.Redis('127.0.0.1', db=1, port=6379, password='')
class CORP_API_TYPE(object):
    GET_APP =['/appapi.aspx', 'GET']
    GET_UserInterface= ['/UserInterface.aspx', 'GET']

class ApiException(Exception) :
    def __init__(self, errCode, errMsg) :
        self.errCode = errCode
        self.errMsg = errMsg

class CorpApi(object) :
    '''
    启动项目入口，
    :return:
    '''
    def __init__(self):
        self.cache = cache
        self.access_token = '00637669729bb167c5a593c99fc0522ca69468f9e701'
        self.corp_api_type = CORP_API_TYPE
        self.username = ''
        self.password = ''
        self.api = CORP_API_TYPE()

    def setAccessToken(self, token):
        self.access_token = token
        self.cache.set('ym_token',token)
    def getAccessToken(self) :
        if self.access_token:
            return self.access_token
        if self.cache.get('ym_token'):
            self.setAccessToken(self.cache.get('ym_token').decode('utf-8'))
            return self.access_token

        return self.refreshAccessToken()

    def refreshAccessToken(self) :
        """
        refresh Access Token
        """
        response = self.httpCall(
            CORP_API_TYPE.GET_APP,
            {'action'  :  'login',
            'username':  self.username,
            'password':  self.password,
            }).text
        token  = response.split('|')[1]
        self.setAccessToken(token)
        return token

    def httpCall(self, urlType, args={}) :
        '''
        :param urlType:
        :param args:
        :param files:
        :return:
        '''
        shortUrl = urlType[0]
        method = urlType[1]
        args.update({
            'token':self.access_token
        })
        if 'POST' == method :
            url = self.__makeUrl(shortUrl)
            response = self.__httpPost(url, args)
        elif 'GET' == method :
            url = self.__makeUrl(shortUrl)
            url = self.__appendArgs(url, args)
            response = self.__httpGet(url)
        else :
            raise ApiException(-1, "unknown method type")
        response.encoding = 'utf-8'
        return response

    @staticmethod
    def __appendArgs(url, args) :
        '''
        :param url:
        :param args:
        :return:
        '''
        for key, value in args.items() :
            if '?' in url :
                url += ('&' + key + '=' + value)
            else :
                url += ('?' + key + '=' + value)
        return url

    @staticmethod
    def __makeUrl(shortUrl) :
        base = HOST
        if shortUrl[0] == '/' :
            return base + shortUrl
        else :
            return base + '/' + shortUrl

    def __appendToken(self, url) :
        if 'TOKEN' in url :
            return url.replace('TOKEN', self.getAccessToken())
        else :
            return url

    def __httpPost(self, url, args) :
        realUrl = self.__appendToken(url)

        return requests.post(realUrl, data=json.dumps(args)).json()

    def __httpGet(self, url) :
        realUrl = self.__appendToken(url)
        return requests.get(realUrl)

    def __post_file(self, url, media_file):
        return requests.post(url, file=media_file).json()

    @staticmethod
    def __checkResponse(response):
        error_data = {
            1001: '参数token不能为空',
            1002: '参数action不能为空',
            1003:'参数action错误',
            1004: 'token失效',
            1005: '用户名或密码错误',
            1006: '用户名不能为空',
            1007: '密码不能为空',
            1008: '账户余额不足',
            1009: '账户被禁用',
            1010: '参数错误',
            1011: '账户待审核',
            1012: '登录数达到上限',
            2001: '参数itemid不能为空',
            2002: '项目不存在',
            2003: '项目未启用',
            2004: '暂时没有可用的号码',
            2005: '获取号码数量已达到上限',
            2006: '参数mobile不能为空',
            2007: '号码已被释放',
            2008: '号码已离线',
            2009: '发送内容不能为空',
            2010: '号码正在使用中',
            3001: '尚未收到短信',
            3002: '等待发送',
            3003: '正在发送',
            3004: '发送失败',
            3005: '订单不存在',
            3006: '专属通道不存在',
            3007: '专属通道未启用',
            3008: '专属通道密码与项目不匹配',
            9001: '系统错误',
            9002: '系统异常',
            9003: '系统繁忙',
        }
        return response

    @staticmethod
    def __tokenExpired(errCode) :
        if errCode == 40014 or errCode == 42001 or errCode == 42007 or errCode == 42009 :
            return True
        else :
            return False

    def __refreshToken(self, url) :
        if 'SUITE_ACCESS_TOKEN' in url :
            self.refreshSuiteAccessToken()
        elif 'PROVIDER_ACCESS_TOKEN' in url :
            self.refreshProviderAccessToken()
        elif 'ACCESS_TOKEN' in url :
            self.refreshAccessToken()
    ###############PUbLIC fun###############################
    def get_userinfo(self):
        response = self.httpCall(
            CORP_API_TYPE['USER_INFO'],{}).text
        self.userinfo={
            'username':response.split('|')[1],
            'status': response.split('|')[2],
            'level': response.split('|')[3],
            'money': response.split('|')[4],
            'frozen_many': response.split('|')[5],
            'discount': response.split('|')[6],
            'max_phone': response.split('|')[7],
        }
    def search_proj(self,keyword):
        params = {
            'actionid':'itemseach',
            'itemname':keyword
        }
        response = self.httpCall(
            CORP_API_TYPE['SEARCH_PROJ'],params).json()
        record = response['data']['list']
        return record

    def get_phone(self,pid,excludeno='170'):
        '''
            获取手机号 872
        '''
        params = {'action':'getmobile',
            'itemid': str(pid),
            'excludeno':excludeno
            }
        response = self.httpCall(
            CORP_API_TYPE.GET_UserInterface,params).text
        print(response)
        phone = response.split('|')[1]
        return phone
    def get_msg(self,pid,phone):
        '''
        :param:pid：项目编号
        :param:phone
        :return:
        '''
        params = {
            'action': 'getsms',
            'itemid':str(pid),
            'mobile':str(phone),
            'release':'1'

        }
        response = self.httpCall(CORP_API_TYPE.GET_UserInterface,params).text
        return response
    def send_msg(self,pid,phone,sms):
        action = 'sendsms'
        params = {
            'action': action,
            'itemid':pid,
            'sms':sms,
            'mobile':phone
        }
        response = self.httpCall(
            self.api.GET_UserInterface,params
        ).text
        return response
    def get_result_by_sendMsg(self,pid,phone):
        '''
            获取发送短信结果
        '''
        action = 'getsendsmsstate'
        params = {
            'action': action,
            'itemid': pid,
            'mobile': phone
        }
        response = self.httpCall(
            self.api.GET_UserInterface, params
        ).text
        return response
    def release(self,pid,phone):
        action = 'release'
        params = {
            'action':action,
            'itemid':pid,
            'mobile':phone
        }
        response = self.httpCall(
            self.api.GET_UserInterface,params
        )
        return response
    def addignore(self,pid,phone):
        '''
        拉黑手机号
        '''
        action = 'addignore'
        params = {
            'action': action,
            'itemid': pid,
            'mobile': phone
        }
        response = self.httpCall(
            self.api.GET_UserInterface,params
        )
        return response

CorpApi= CorpApi()