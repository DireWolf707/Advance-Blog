from django.urls import path
from .views import PostDetail,PostList,PostShare,SearchView
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('',PostList.as_view(),name='post_list'),
    path('search/',SearchView.as_view(),name='post_search'),
    path('tag/<slug:slug>/',PostList.as_view(),name='post_list_by_tag'),
    path('<int:pk>/share/',PostShare.as_view(),name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',PostDetail.as_view(),name='post_detail'),
    path('feed/',LatestPostsFeed(),name='post_feed'),
]
