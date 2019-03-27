import os
import sys
import time
from datetime import datetime,timedelta
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from shop.tasks import qiaohuRecommended_beat