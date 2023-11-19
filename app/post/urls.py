from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post import views

router = DefaultRouter()
router.register('', views.PostViewSet)
router.register(r'comments', views.CommentViewSet, basename='comment')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls))
]