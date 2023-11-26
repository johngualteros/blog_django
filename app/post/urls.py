from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post import views

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]