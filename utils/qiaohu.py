from Public.YMCorpApi import CorpApi as YmCorp
import requests
from bs4 import BeautifulSoup
import random
import json
import random
import string
import time


from celery.utils.log import get_task_logger
logger = get_task_logger('beat')

from utils.baiduapi import handwriteRecog



def random_name(size=1, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def first_name(size=2, ln=None, fn=None):
    _lst = []
    for i in range(size):
        _item = random_name(1, fn)
        if ln:
            while _item in ln:
                _item = random_name(1, fn)
            _lst.append(_item)
        else:
            _lst.append(_item)
    return "".join(_lst)
def last_name(size=1, names=None):
    return random_name(size, names)
def full_name(lns, fns):
    _last = last_name(1, lns)
    return "{}{}".format(_last, first_name(random.randint(1, 2), _last, fns))

def generate_name():
    last_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
                      '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
                      '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
                      '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
                      '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
                      '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
                      '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']

    first_names = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
                       '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
                       '会', '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于', '心', '学', '么', '之', '都', '好',
                       '看', '起', '发', '当', '没', '成', '只', '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
                       '总', '从', '无', '情', '己', '面', '最', '女', '但', '现', '前', '些', '所', '同', '日', '手', '又', '行', '意', '动',
                       '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯', '知',
                       '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其', '进', '此', '话', '常', '与', '活', '正', '感',
                       '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西', '果', '走',
                       '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三', '机', '工', '物', '气', '每', '并', '别', '真', '打',
                       '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电', '主', '界', '门',
                       '利', '海', '受', '听', '表', '德', '少', '克', '代', '员', '许', '稜', '先', '口', '由', '死', '安', '写', '性', '马',
                       '光', '白', '或', '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神', '记', '处', '让', '母',
                       '父', '应', '直', '字', '场', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军',
                       '候', '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快', '原',
                       '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢',
                       '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片', '罗',
                       '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合', '反',
                       '题', '必', '该', '论', '交', '终', '林', '请', '医', '晚', '制', '球', '决', '窢', '传', '画', '保', '读', '运', '及',
                       '则', '房', '早', '院', '量', '苦', '火', '布', '品', '近', '坐', '产', '答', '星', '精', '视', '五', '连', '司', '巴',
                       '奇', '管', '类', '未', '朋', '且', '婚', '台', '夜', '青', '北', '队', '久', '乎', '越', '观', '落', '尽', '形', '影',
                       '红', '爸', '百', '令', '周', '吧', '识', '步', '希', '亚', '术', '留', '市', '半', '热', '送', '兴', '造', '谈', '容',
                       '极', '随', '演', '收', '首', '根', '讲', '整', '式', '取', '照', '办', '强', '石', '古', '华', '諣', '拿', '计', '您',
                       '装', '似', '足', '双', '妻', '尼', '转', '诉', '米', '称', '丽', '客', '南', '领', '节', '衣', '站', '黑', '刻', '统',
                       '断', '福', '城', '故', '历', '惊', '脸', '选', '包', '紧', '争', '另', '建', '维', '绝', '树', '系', '伤', '示', '愿',
                       '持', '千', '史', '谁', '准', '联', '妇', '纪', '基', '买', '志', '静', '阿', '诗', '独', '复', '痛', '消', '社', '算',
                       '义', '竟', '确', '酒', '需', '单', '治', '卡', '幸', '兰', '念', '举', '仅', '钟', '怕', '共', '毛', '句', '息', '功',
                       '官', '待', '究', '跟', '穿', '室', '易', '游', '程', '号', '居', '考', '突', '皮', '哪', '费', '倒', '价', '图', '具',
                       '刚', '脑', '永', '歌', '响', '商', '礼', '细', '专', '黄', '块', '脚', '味', '灵', '改', '据', '般', '破', '引', '食',
                       '仍', '存', '众', '注', '笔', '甚', '某', '沉', '血', '备', '习', '校', '默', '务', '土', '微', '娘', '须', '试', '怀',
                       '料', '调', '广', '蜖', '苏', '显', '赛', '查', '密', '议', '底', '列', '富', '梦', '错', '座', '参', '八', '除', '跑',
                       '亮', '假', '印', '设', '线', '温', '虽', '掉', '京', '初', '养', '香', '停', '际', '致', '阳', '纸', '李', '纳', '验',
                       '助', '激', '够', '严', '证', '帝', '饭', '忘', '趣', '支', '春', '集', '丈', '木', '研', '班', '普', '导', '顿', '睡',
                       '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭', '创', '区', '奥', '器', '谢', '弟', '店', '否',
                       '害', '草', '排', '背', '止', '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河', '续',
                       '哥', '呼', '若', '推', '境', '遇', '雨', '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪', '索',
                       '剧', '啊', '船', '险', '烟', '依', '斗', '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族', '低',
                       '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团', '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅', '街',
                       '劳', '型', '烈', '姑', '陈', '莫', '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀', '律',
                       '胜', '份', '汽', '右', '洋', '范', '床', '舞', '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职', '属',
                       '渐', '左', '录', '丝', '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉', '遗',
                       '救', '修', '松', '临', '藏', '担', '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳', '差',
                       '短', '祖', '云', '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府', '压',
                       '超', '负', '勒', '杂', '醒', '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童', '顶',
                       '派', '素', '脱', '农', '疑', '练', '野', '按', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯', '巨',
                       '琴', '免', '环', '姆', '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层', '付',
                       '阵', '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀', '营',
                       '退', '摇', '弄', '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '优', '课', '鸟', '喊', '降',
                       '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰',
                       '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡', '预',
                       '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误',
                       '乾', '坤']
    return full_name(last_names, first_names)

def generate_bb():
    '''
      生成宝宝生日
    '''
    year = random.choice(range(2012,2017))
    month = random.choice(range(10,12))
    day = random.choice(range(10,28))
    return year,month,day

def get_addr():
    data = json.load(open('addr.json',encoding = 'utf-8'))
    province_data =random.choice(data)
    province = province_data.get('name')
    city_obj = random.choice(province_data.get('city'))
    city_name = city_obj.get('name')
    county_name = random.choice(city_obj.get('area'))
    return province,city_name,county_name
def generate_addr():
    data = [
    ['湖北省','黄冈市','团风县','湖北省团风中学'],
    ['湖北省','武汉市','洪山区','武汉职业技术学院'],
    ['湖北省','武汉市','武昌区','武昌理工大学'],
    ['湖北省','武汉市','武昌区','武汉大学东10'],
    ['湖北省','武汉市','武昌区','华中科技大学'],
    ['湖北省','武汉市','武昌区','湖北工业大学'],        
    ['湖北省','武汉市','武昌区','武昌理工大学'],
    ['湖北省','武汉市','武昌区','湖北经济学院'],
    ['湖北省','武汉市','武昌区','中南财经政法大学南湖校区'],
    ['湖北省','武汉市','武昌区','武汉工程大学流芳校区'],
    ['湖北省','武汉市','武昌区','华中农业大学'],
    ['湖北省','武汉市','武昌区','湖北第二师范学院'],
    ['湖北省','武汉市','武昌区','武汉体育学院'],
    ['湖北省','武汉市','洪山区','湖北省武汉市洪山区关山大道588号'],
    ['湖北省','武汉市','武昌区','湖北省武汉市汉阳区龙兴东街254号'],
    ]
    return random.choice(data)

def qiaohu_apply(url='',proxy=None):
    s_province,s_city,s_county,af_add = generate_addr()
    pa_name = generate_name()
    bb_year,bb_month,bb_day = generate_bb()
    logger.info("表单信息：%s-%s-%s %s %s 日期:%s-%s-%s"%(s_province,s_city,s_county,af_add,pa_name,bb_year,bb_month,bb_day))
    # 获取一个手机号
    pid = 872
    mobile = YmCorp.get_phone(pid)
    logger.info('手机号:%s' % mobile)

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    session = requests.session()
    if proxy:
      session.proxies = proxy
    formurl = url
    response = session.get(formurl)
    html = BeautifulSoup(response.text,'html.parser')
    csrf_token = html.find(attrs={ 'name':'YII_CSRF_TOKEN'}).attrs['value']
    capt_token = html.find(id='captcha_token').attrs['value']
    way = html.find(attrs={ 'name':'way'}).attrs['value']
    startBBDate = html.find(attrs={ 'name':'startBBDate'}).attrs['value']
    sevenmonth = html.find(attrs={ 'name':'sevenmonth'}).attrs['value']
    twentyfourmonth = html.find(attrs={ 'name':'twentyfourmonth'}).attrs['value']
    addr_url = 'https://tiyan.qiaohu.com/site/getAreacode'
    addr_data = {
        'province':s_province,
        'city':s_city,
        'area':s_county,
        'YII_CSRF_TOKEN':csrf_token
    }
    af_post= session.post(addr_url,data = addr_data).json().get('areacode')
    flag=False
    for rety in range(10):
      capt_url = 'https://tiyan.qiaohu.com/site/captcha?captcha_token={}&reload={}'.format(capt_token,random.random())
      img = session.get(capt_url)
      captcha = handwriteRecog(img.content).strip()
      logger.info('GET CAPTCHA:%s' %captcha)
      if len(captcha)!=4:
          continue
      check_data = {
          'captcha': captcha.strip(),
          'captcha_token': capt_token,
          'YII_CSRF_TOKEN': csrf_token
      }
      check_ajax_url = 'https://tiyan.qiaohu.com/site/ajaxCaptcha'
      ajax_res=session.post(check_ajax_url, data=check_data)
      if ajax_res.text == '0':
          check_capt_url = 'https://tiyan.qiaohu.com/site/captchacheck'
          check_response = session.post(check_capt_url,data=check_data)
          flag=True
          break
    if not flag:
      logger.warn('验证码识别失败超过10次')
      return {'status':False,'msg':'验证码识别失败超过10次'}
    site_index_url = 'https://tiyan.qiaohu.com/site/index'
    data_info = {
        'YII_CSRF_TOKEN':csrf_token,
        'way':way,
        'yuerzs':'1',
        'startBBDate':startBBDate,
        'captcha_token':capt_token,
        'sevenmonth': sevenmonth,
        'twentyfourmonth':twentyfourmonth,
        'pa_name': pa_name, #父亲信息
        'bb_year':bb_year,  #宝宝年月
        'bb_month':bb_month,## 00
        'bb_day':bb_day,    ## 00
        'af_mobile':mobile,  ## 手机
        's_province':s_province,##省份
        's_city':s_city,  #市
        's_county':s_county,#镇
        'City_Save':'',
        'af_add':af_add, # 详细地址
        'af_post':af_post,
        'captcha':captcha
        }

    resp = session.post(site_index_url,data = data_info)
    if "请输入发送到您手机的认证码" in resp.text:
        session.get(site_index_url)
        checkcode_url = 'https://tiyan.qiaohu.com/site/checkcode'
        sms_flag = False
        for ret in range(60):
            code = YmCorp.get_msg(pid,mobile)
            if str(code) == '3001' or str(code) == '2007':
                time.sleep(2)
            else:
                code = code[-4:]
                logger.info('手机号：%s 成功获取验证码：%s！' %(mobile,code))
                sms_flag = True
                break
        if not sms_flag:
          logger.info('手机号：%s 获取验证码错误' %(mobile))
          return {'status':False,'msg':'手机验证码获取错误'}
        code_data = {
            'checkcode':str(code),
            'YII_CSRF_TOKEN':csrf_token
            }
        result_resp = session.post(checkcode_url,data = code_data)
        try:
            status = result_resp.json().get('status')
            msg = result_resp.json().get('message')
            return {'status':status,'msg':msg}
        except Exception as e:
            status = False
            msg = e
            timestamp = str(int(time.time())) + '.html'
            with open(timestamp, 'w', encoding='utf-8') as f:
                f.write(resp.text)
            return {'status':status,'msg':msg+timestamp}
    elif '刷新频繁，请稍后再试' in resp.text:
      logger.warn('提交数据错误：刷新频繁，请稍后再试')
      return {'status':False,'msg':'刷新频繁，请稍后再试'}
    else:
      tiemstamp = str(int(time.time()))+'.html'
      with open(tiemstamp,'w',encoding='utf-8') as f:
        f.write(resp.text)
      logger.warn('信息提交失败,htmlFile%s' % tiemstamp)
      return {'status':False,'msg':'信息提交失败'}



# result = qiaohu_apply()
# print(result)

