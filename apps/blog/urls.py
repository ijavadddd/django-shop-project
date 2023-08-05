from django.urls import path
from .views import BlogView, PostView, LatestPostsPartial


app_name = 'blog'
urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('post/<int:id>/<slug:slug>/', PostView.as_view(), name='post'),
    path('latest-posts/', LatestPostsPartial.as_view(), name='latest_posts'),
]
