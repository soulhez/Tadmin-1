from django.db import models
import uuid,re
import datetime
from django.db.models.query import QuerySet
#base model

class CoreManager(models.Manager):
    u'''覆盖原来的查询, 应该考虑去除，这样增加了程序的复杂度'''
    def get_queryset(self):
        return QuerySet(self.model,using=self._db).filter(is_del=1)


class CoreModel(models.Model):
    DELETE_FLG_CHOICE = (
        (1, u'正常'),
        (0, u'已删除'),
    )
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36,verbose_name='创建时间')
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_del = models.CharField(
        u'删除标记', max_length=5, null=True, blank=True, editable=False,
        choices=DELETE_FLG_CHOICE, default=1)
    objects = CoreManager()
    _logic_delete = True
    def delete(self, *args, **kwargs):
        u'''逻辑删除'''
        if self._logic_delete:
            self.mtime = datetime.datetime.now()
            self.is_del = 0
            self.save(*args, **kwargs)
        else:
            self.remove()

    def remove(self, *args, **kwargs):
        u'''在逻辑删除下的物理删除'''
        return super(CoreModel, self).delete(*args, **kwargs)
    class Meta:
        abstract = True