from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from django.views.generic import ListView,View,FormView
from .forms import EmailForm
from django.contrib import messages
from django.core.mail import send_mail

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
    
class PostShare(FormView):
    form_class = EmailForm
    template_name = 'share.html'
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        post = get_object_or_404(Post,id=self.kwargs['pk'])
        
        #preparing email after validating data
        post_url = self.request.build_absolute_uri(
            post.get_absolute_url()
        )
        subject = f"{form_data['name']} recommended you to read {post.title}"
        message = f"Read {post.title} at {post_url}"
        if form_data['comments']:
            message += f"\n\n{form_data['name']}'s comments : {form_data['comments']}"
            
        #sending email after validating data  
        send_mail(subject,message,'admin@mail.com',(form_data['to'],))
        
        #adding succeess message
        messages.success(self.request, 'Post Shared Successfully !')
        return redirect('blog:post_share',self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post,id=self.kwargs['pk'])
        return context
    