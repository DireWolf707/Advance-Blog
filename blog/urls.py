from django.urls import path
from .views import PostDetail,PostList,PostShare
app_name = 'blog'

urlpatterns = [
    path('',PostList.as_view(),name='post_list'),
    path('tag/<slug:slug>/',PostList.as_view(),name='post_list_by_tag'),
    path('<int:pk>/share/',PostShare.as_view(),name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',PostDetail.as_view(),name='post_detail'),
]
