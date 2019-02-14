from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication,BaseAuthentication,get_authorization_header
import datetime
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache

import logging
logger = logging.getLogger("django") # 为loggers中定义的名称


class ExpiringTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        tokens = [token for token in
                  [request.META.get('HTTP_AUTHORIZATION'),
                   request.data.get('authorization', None) if isinstance(request.data, dict) else None,
                   request.query_params.get('authorization', None)]
                  if token is not None]
        if len(tokens) == 0:
            raise AuthenticationFailed

        token_cache = 'token_' + tokens[0]
        token = cache.get(token_cache)
        if token:
            if not token.user.is_active:
                raise AuthenticationFailed('用户被禁止')
            utc_now = datetime.datetime.utcnow()
            if token.created.replace(tzinfo=None) < utc_now - datetime.timedelta(hours=24 * 7):  # 设定存活时间 14天
                token.delte()
                raise exceptions.AuthenticationFailed('认证信息过期')
            return (token.user, None)
        else:
            raise AuthenticationFailed('认证失败')


