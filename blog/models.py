from django.db import models
from django.utils import timezone
from account.models import UserProfile
User=UserProfile
ARTICLE_FROM = {
    0: u'原创',
    1: u'转载',
}
STATUS = {
    0: u'发表',
    1: u'草稿',
    2: u'丢弃',
}
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'类型名称')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
    class Meta:
        verbose_name = u'文章类型'
        verbose_name_plural = verbose_name
        ordering = ['rank','-create_time']

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'标签',default='')
    create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)

    class Meta:
        verbose_name = u'文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(User,verbose_name=u'作者',on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category,verbose_name=u'类型',on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=50,verbose_name=u'标题')
    article_from = models.IntegerField(default=0,choices=ARTICLE_FROM.items(),verbose_name=u'文章来源',null=True)
    summary = models.TextField(verbose_name=u'摘要',null=True,blank=True)
    # tags=models.ManyToManyField(Tag,verbose_name="标签",blank=True,null=True)
    content = models.TextField(verbose_name="正文")
    # edit_type = models.IntegerField(default=0, choices=edit_type.items(), verbose_name=u'编辑方式')
    reading_num = models.IntegerField(default=0,verbose_name=u'阅读量')
    praise_num = models.IntegerField(default=0, verbose_name=u'点赞数')
    is_top = models.BooleanField(default=False,verbose_name=u'是否置顶')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name=u'文章状态')
    summary_img=models.URLField(null=True,verbose_name="文章主图",blank=True)
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间', blank=True,auto_now=True)

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    # def get_absolute_url(self):
    #     from django.core.urlresolvers import reverse
    #     return reverse('article-view', args=(self.en_title,))

    def get_category(self):
        return self.category

    def __str__(self):
        return self.title