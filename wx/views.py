from django.shortcuts import render,HttpResponse

from utils.wx.WXMsgCrypt import  WXBizMsgCrypt
# Create your views here.
Token = 'TjivA86NJ'
EncodingAESKey = '8GHmwN12PUONYQzvXjhAL5pqUvJaQOkVbUtO7JIWtwY'
CorpID = 'wwcce9bb042e7b644e'
import xml.etree.cElementTree as ET
wxcpt=WXBizMsgCrypt(Token,EncodingAESKey,CorpID)
# Create your views here.

def server(request):
    if request.method == 'GET':
        # 这里改写你在微信公众平台里输入的token
        # 获取输入参数
        data = request.GET
        msg_signature = data.get('msg_signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        ret, EchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        if ret == 0:
            return HttpResponse(EchoStr)
        else:
            pass
    else:
        msg_signature = request.GET.get('msg_signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        reqdata = request.body.decode('iso8859-1')
        ret,Msg=wxcpt.DecryptMsg( reqdata, msg_signature, timestamp, nonce)
        xml_tree = ET.fromstring(Msg)
        return HttpResponse("OK")


