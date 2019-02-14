import logging
import re

from django import http
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import mail_managers
from django.urls import is_valid_path
from django.utils.cache import get_conditional_response, set_response_etag
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import force_text


logger = logging.getLogger('django.request')

class PermissionUrlMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Check for denied User-Agents and rewrite the URL based on
        settings.APPEND_SLASH and settings.PREPEND_WWW
        """
        path=request.get_full_path(force_append_slash=True)
        print(path)
        return None