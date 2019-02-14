from django.urls import path, include
from rest_framework import routers
from API.admin.user.views import UserViewSet,RoleViewSet,MenuViewSet
from API.admin.shop.views import CourseViewSet,ImoocViewSet,LangViewSet,ResViewSet,qiaohuOrderViewSet,\
    qiaohuRecordViewSet,WalfareSexxViewSet,FunServerViewSet,CategoryViewSet

from API.admin.shop import views as admin_shop_viewset
from API.admin.blog.views import ArticleViewSet,TagViewSet,CategoryViewSet
from API.admin.user.views import AdminLogin,Logout
from API.admin import shop



#user
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'role', RoleViewSet)
router.register(r'menu',MenuViewSet)

#shop
router.register(r'imooc', ImoocViewSet)
router.register(r'funserver', FunServerViewSet)
router.register(r'imooclang', LangViewSet)
router.register(r'yunpan', ResViewSet)
router.register(r'shop/qiaohuorder', qiaohuOrderViewSet)
router.register(r'shop/qiaohurecord', qiaohuRecordViewSet)
router.register(r'shop/kdw', WalfareSexxViewSet)
router.register(r'shop/course', CourseViewSet)
router.register(r'shop/category',admin_shop_viewset.CategoryViewSet )
router.register(r'shop/attribute',admin_shop_viewset.AttributeViewSet )


#blog
router.register(r'blog/article', ArticleViewSet)
router.register(r'blog/category', TagViewSet)
router.register(r'blog/tag', CategoryViewSet)
router.register(r'pandownload',shop.views.PandownloadViewset,base_name="pandownload")

from API.admin import views
app_name="admin"
urlpatterns = [
    path('qiniu_token/',views.qiniuViews.as_view()),
    path('login/', AdminLogin.as_view()),
    path('logout/',Logout.as_view()),
    path('',include(router.urls)),
]