from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView,View

class PostList(ListView):
    queryset = Post.published.all()
    template_name = 'list.html'
    context_object_name = 'posts'
    paginate_by = 3
    
class PostDetail(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post,
                                 slug = kwargs['slug'],
                                 status = 'published',
                                 publish__year = kwargs['year'],
                                 publish__month = kwargs['month'],
                                 publish__day = kwargs['day']
                                 )
        
        return render(request,'detail.html',{'post':post})