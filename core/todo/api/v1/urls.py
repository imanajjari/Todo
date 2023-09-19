from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', views.PostModelViewset, basename = 'post')
router.register('category', views.CategoryModelViewset, basename = 'category')

app_name = 'api-v1'
urlpatterns = [
]
urlpatterns += router.urls 