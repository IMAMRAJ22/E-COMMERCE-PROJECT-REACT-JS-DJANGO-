from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginViewSet,CartViewSet,ItemViewSet,BuyViewSet,SaveViewSet,LikeViewSet,UploadExcelView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views


router = DefaultRouter()
router.register('users', LoginViewSet)
router.register('cart',CartViewSet)
router.register('item',ItemViewSet)
router.register('buy',BuyViewSet)
router.register('save', SaveViewSet)
router.register('like',LikeViewSet)
urlpatterns = [
    path('', include(router.urls)),
    #excel
    path("upload-excel/", UploadExcelView.as_view(), name="upload-excel"),
]