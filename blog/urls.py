from django.urls import path
from .views import PostDetail,PostList
app_name = 'blog'

urlpatterns = [
    path('',PostList.as_view(),name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',PostDetail.as_view(),name='post_detail'),
]
