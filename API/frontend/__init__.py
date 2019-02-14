#
from rest_framework import routers
from API.frontend.user.views import UserViewSet,RoleViewSet
from API.frontend.shop.views import CourseViewSet,ImoocViewSet,LangViewSet,ResViewSet,qiaohuOrderViewSet,\
    qiaohuRecordViewSet,WalfareSexxViewSet,FunServerViewSet,WeiboAPIViewSet
from API.frontend.blog.views import ArticleViewSet,TagViewSet,CategoryViewSet
from django.urls import path, include
from API.frontend.user.views import CustomAuthToken,Register



#user
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'role', RoleViewSet)

#shop
router.register(r'imooc', ImoocViewSet)
router.register(r'funserver', FunServerViewSet)
router.register(r'imooclang', LangViewSet)
router.register(r'yunpan', ResViewSet)
router.register(r'qiaohuorder', qiaohuOrderViewSet)
router.register(r'qiaohurecord', qiaohuRecordViewSet)
router.register(r'welfaresexx', WalfareSexxViewSet)
router.register(r'course', CourseViewSet)
router.register(r'weiboapi', WeiboAPIViewSet)



#blog
router.register(r'article', ArticleViewSet)
router.register(r'category', TagViewSet)
router.register(r'tag', CategoryViewSet)


app_name='forntend'
urlpatterns = [
    path('',include(router.urls)),
    path('login/',CustomAuthToken.as_view()),
    path('register/', Register.as_view()),
]
