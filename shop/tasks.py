from __future__ import absolute_import
import os, django
import sys
#sys.path.append('D:\Coding\TAdmin-django')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','Settings.Prod')
#django.setup()

from  utils.qiaohu import qiaohu_apply
from celery import shared_task,task
from django.db.models import F
from shop.models import qiaohuOrder,qiaohuRecord
import logging
from celery.utils.log import get_task_logger
logger = get_task_logger('task')

@shared_task
def qiaohu_order(oid):
    oid = 'b1541a94-db56-48f4-8100-1f89a1d94149'
    order = qiaohuOrder.objects.filter(id=oid).first()
    url = order.url
    print(order)
@shared_task(expires=600)
def qiaohuRecommended_beat():
    '''
     自动获取未完成订单 进行自动申请
    '''
    #获取任务 每次获取一个  目前没有代理的情况下
    order = qiaohuOrder.objects.filter(is_pay=True,order_num__gt=F('completed')).first()
    if not order:
        return
    logger.info("order:%s url:%s" % (order.id, order.url))
    try:
        result = qiaohu_apply(order.url)
    except Exception as e:
        logger.error(e)
        result = {
            'status':False,
            'msg':e,
            'order':order
        }
    logger.info(result)
    if result['status']:
        order.completed = order.completed + 1
    order.save()
    # insert record
    qiaohuRecord.objects.create(**{
        'is_ok':result['status'],
        'msg': result['msg'],
        'order':order
    })
@shared_task
def add():
    logger.info('this is logger of add funcation')
    return 3
