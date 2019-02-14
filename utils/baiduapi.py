from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '11554381'
API_KEY = 'SjvBRy3meqwH7b2bjrSbnAq3'
SECRET_KEY = 'kgq2FdPQqxCprXhcc5sKASEAmOkvskkG'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
def handwriteRecog(image):
    '''
        文字识别
    '''
    """ 调用通用文字识别（高精度版） """
    client.basicAccurate(image);
    """ 如果有可选参数 """
    options = {}
    """ 带参数调用通用文字识别（高精度版） """
    result=client.basicAccurate(image, options)
    return result.get('words_result',['null'])[0].get('words','null')
# word=handwriteRecog('1.jpg')
