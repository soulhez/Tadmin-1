
from django.db import models
from API.models import CoreModel
from account.models import UserProfile
User=UserProfile

# Create your models here.

STATUS = (
(0, '已上架'),
(1, '未上架'),
(2,  '待审核')
)



class lang(models.Model):
    id = models.AutoField(primary_key=True)
    en = models.CharField(max_length=64)
    cn = models.CharField(max_length=64)
    logo = models.CharField(max_length=64)
    show = models.BooleanField(default=True)
    class Meta():
        db_table = 'shop_lang'




class imooc(models.Model):
    '''
        慕课网资源
    '''
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,verbose_name='标题')
    desc = models.CharField(max_length=255,verbose_name='描述')
    content = models.TextField(null=True)
    price = models.FloatField(null=True)
    stock = models.IntegerField(null=True)
    sales = models.IntegerField(null=True,verbose_name='销量')
    default_img = models.CharField(max_length=255,verbose_name='主图')
    status = models.IntegerField(default=0,null=True, choices=STATUS, verbose_name=u'文章状态')
    lang = models.ForeignKey(lang,to_field='id',on_delete=models.CASCADE,related_name='lang')
    url = models.CharField(max_length=255,null=True,verbose_name='来源')
    res  = models.CharField(max_length=255,null=True,verbose_name='资源',blank=True)
    spare_res = models.CharField(max_length=255, null=True, verbose_name='备用资源')
    seralizer_field = ('id','title','desc','content','price','stock','sales','default_img','status','lang','url','res','spare_res')
    class Meta():
        db_table = 'shop_imooc'

#

class resource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,null=True)
    url = models.CharField(max_length=255)
    source = models.CharField(max_length=255,null=True,verbose_name='refer')
    code = models.CharField(max_length=32,null=True)
    size = models.CharField(max_length=32,null=True,verbose_name='大小')
    share_time = models.CharField(max_length=62,null=True,verbose_name='分享时间')
    col_time = models.DateTimeField(auto_now=True,verbose_name='采集时间')
    class Meta():
        db_table = 'shop_res'
    serialize_field = ('id','title','url','source','code','size','share_time','col_time')

class funServer(models.Model):
    '''
    服务信息
    '''
    en =models.CharField(max_length=255,primary_key=True,verbose_name='名称简写')
    name = models.CharField(max_length=255,null=True,verbose_name='服务名称')
    ishsow = models.BooleanField(default=True)
    img = models.CharField(max_length=255,null=True)
    summary = models.CharField(max_length=255,null=True,verbose_name='简介')
    sale = models.IntegerField(default=0,verbose_name='已售')
    price = models.FloatField(null=True,verbose_name='售价')

class qiaohuOrder(CoreModel):
    '''
       巧虎服务短信订单
    '''
    user = models.ForeignKey(User,null=True,verbose_name='申请用户',on_delete=models.CASCADE)
    pay_type = models.CharField(max_length=255,verbose_name='支付方式',null=True)
    order_num =models.IntegerField(default=0,verbose_name='数量')
    order_price = models.FloatField(default=0,verbose_name='总价格')
    is_pay = models.BooleanField(default=False)
    source = models.CharField(max_length=255,null=True,verbose_name='来源')
    url = models.CharField(max_length=255,verbose_name='巧虎链接')
    completed = models.IntegerField(default=0,verbose_name='已完成')
    remark=models.CharField(max_length=255,verbose_name='备注')
    class Meta:
        pass
    def email(self):
        return self.user.email if self.user else ''

class qiaohuRecord(CoreModel):
    '''
        巧虎执行记录
    '''
    order = models.ForeignKey(qiaohuOrder,verbose_name='订单',on_delete=models.CASCADE)
    data = models.CharField(max_length=255,verbose_name='申请信息',null=True)
    is_ok = models.BooleanField(default=True,verbose_name='完成状况')
    msg = models.CharField(max_length=255,null=True,verbose_name='执行结果')
    class Meta:
        pass

class welfaresexx(models.Model):
    id = models.AutoField(primary_key=True)
    videoid = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    url=models.CharField(max_length=255)
    upload_time =models.DateTimeField(null=True)
    index_img =models.CharField(max_length=255,blank=True,null=True)
    vote_num=models.IntegerField(null=True)
    praise_rate=models.CharField(max_length=255,blank=True,null=True)
    video_time=models.CharField(max_length=255,blank=True,null=True)
    views_num=models.IntegerField(null=True)
    summary=models.TextField(null=True,blank=True)
    classes=models.CharField(max_length=255,blank=True,null=True)
    tags=models.CharField(max_length=255,blank=True,null=True)
    video_img=models.CharField(max_length=255,blank=True,null=True)
    video_size=models.CharField(max_length=255,blank=True,null=True)
    video_url=models.CharField(max_length=255,blank=True,null=True)
    ctime=models.DateTimeField(null=True)
    serializer_fields = ('id','videoid','title','url','upload_time','index_img','index_img','vote_num','praise_rate','video_time','views_num','summary','classes','tags','video_img','video_size','video_url','ctime')
    class Meta:
        db_table = 'welfare_sexx'



class Course(models.Model):
    '''
        通用教程  其他的在此基础扩展
    '''
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,verbose_name='标题',unique=True)
    desc = models.CharField(max_length=255,verbose_name='描述')
    content = models.TextField(null=True,verbose_name='内容')
    tags = models.CharField(max_length=255,null=True,verbose_name='标签')
    default_img = models.CharField(max_length=255,verbose_name='主图')
    source_name = models.CharField(max_length=255,null=True,verbose_name='来源网站')
    source_url = models.CharField(max_length=255,verbose_name='来源连接',null=True)
    res  = models.CharField(max_length=255,null=True,verbose_name='资源',blank=True)
    remark = models.CharField(max_length=255, null=True, verbose_name='备注',blank=True)

    price = models.FloatField(verbose_name='售价', null=True)
    sales = models.IntegerField(verbose_name='已售', null=True)
    online = models.IntegerField(verbose_name='是否上线', default=1)

    class Meta():
        db_table = 'shop_course'

#
# class TBCourse(models.Model):
#     '''
#         商品名称可以和 资源名称不一致
#     '''
#     id=models.AutoField(primary_key=True)
#     course = models.ForeignKey(Course,null=True,on_delete=models.SET_NULL,unique=True)
#     title = models.CharField(max_length=255,verbose_name='淘宝标题')
#     classification = models.CharField(max_length=255,verbose_name='淘宝分类',null=True)
#     tburl = models.CharField(max_length=255,verbose_name='淘宝连接',null=True)
#     price = models.FloatField(verbose_name='售价',null=True)
#     sales = models.IntegerField(verbose_name='已售',null=True)
#     content = models.TextField(verbose_name='内容',null=True)
#     frist_img = models.CharField(max_length=255,verbose_name='首图',null=True)
#     online = models.IntegerField(verbose_name='是否上线',default=1)
#
#
#
#     serialize_field = ('id','course','title','classification','tburl','price','sales','content','frist_img','online')

# class Goods(models.Model):
#     '''商品基类'''
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=255, verbose_name='淘宝标题')
#     price = models.FloatField(verbose_name='售价', null=True)
#     sales = models.IntegerField(verbose_name='已售', null=True)
#     content = models.TextField(verbose_name='内容', null=True)
#     frist_img = models.CharField(max_length=255, verbose_name='首图', null=True)
#     online = models.IntegerField(verbose_name='是否上线', default=1)
#     class Meta:
#         abstract = True

# class GoodsOrder(CoreModel):
#     '''订单表'''
#     STATUS_CHOICES=(
#         (10,"未支付"),
#         (20,"待发货"),
#         (30,"待收货"),
#         (40, "待评价"),
#         (50, "已完成")
#     )
#     GOODS_TYPES_CHOICES=(
#         (10,"网课视频"),
#         (20,"其他")
#     )
#     status=models.IntegerField(choices=STATUS_CHOICES)
#     user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
#     price = models.FloatField(verbose_name='价格')
#     count = models.IntegerField(default=1, verbose_name='商品数量')
#     goods_id = models.IntegerField(verbose_name='商品id')
#     goods_type = models.IntegerField(choices=GOODS_TYPES_CHOICES,verbose_name='商品分类')
#     addr = models.ForeignKey('user.Address', verbose_name='地址', on_delete=models.CASCADE)
#     trade_no = models.CharField(max_length=128, default='', verbose_name='支付编号')
#
#     class Meta:
#         verbose_name = '订单'
#         verbose_name_plural = verbose_name
#
#


'''常规电商数据库设计'''

class Category(models.Model):
    id=models.AutoField(primary_key=True)
    label= models.CharField(max_length=255,verbose_name='名称')
    pid=models.ForeignKey('self',verbose_name='父亲',on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        verbose_name = '商城分类'
        verbose_name_plural = verbose_name



class Goods(models.Model):
    STATUS_CHOICE=(
        (10,"上架"),
        (20, "下架"),
    )
    id=models.AutoField(primary_key=True,verbose_name='商品id')
    title= models.CharField(max_length=255,verbose_name='商品标题')
    detail=models.TextField(verbose_name='描述')
    cate=models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='价格')
    stock = models.IntegerField(verbose_name="库存")
    status=models.IntegerField(choices=STATUS_CHOICE,verbose_name='状态',default=10)
    image_url=models.CharField(max_length=255,verbose_name='封面图片')
    sales=models.IntegerField(default=0,verbose_name='销量')


class Attribute(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.ForeignKey(Category,verbose_name="分类",on_delete=models.CASCADE)
    name=models.CharField(verbose_name="属性名称",max_length=255)
    class Meta:
        verbose_name = '系统规格表'
        verbose_name_plural = verbose_name

class Attribute_Value_Goods(models.Model):
    id=models.AutoField(primary_key=True)
    goods=models.ForeignKey(Goods,verbose_name='商品',on_delete=models.CASCADE)
    attribute=models.ForeignKey(Attribute,verbose_name='规格',on_delete=models.CASCADE,max_length=255)
    value=models.CharField(max_length=255,verbose_name='选项值')
    class Meta:
        verbose_name = '商品规格值绑定'
        verbose_name_plural = verbose_name



class WeiboAPi(models.Model):
    '''微博登录接口'''
    RESULT_SUCCESS="登录成功"
    RESULT_FAILD="登录失败"

    RESULT_CHOICES=(
        ("登录成功","登录成功"),
        ("登录失败", "登录失败"),
    )


    id=models.AutoField(primary_key=True)
    phone=models.CharField(max_length=32,verbose_name='微博手机号')
    password=models.CharField(max_length=255,verbose_name='微博密码')
    result_msg=models.CharField(max_length=4096,verbose_name='登录消息')
    result_status=models.CharField(choices=(RESULT_CHOICES),verbose_name="登录结果",max_length=255)
    login_ip=models.CharField(max_length=255,verbose_name='登录ip')
    create_ip=models.CharField(max_length=255,verbose_name='申请ip')
    login_datetime=models.DateTimeField(max_length=255,auto_created=True)