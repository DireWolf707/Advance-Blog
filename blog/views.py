from django.contrib.postgres import search
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from taggit.models import Tag
from django.views.generic import ListView,View,FormView
from .forms import EmailForm,CommentForm,SearchForm
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank

class PostList(ListView):
    template_name = 'list.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_queryset(self):
        querySet = Post.published.all()
        tag = self.kwargs.get('slug',0)
        if tag:
            tag = get_object_or_404(Tag,slug=tag)
            querySet = querySet.filter(tags__in=[tag])
        return querySet
    
class PostDetail(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request,'detail.html',context=context)
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            return self.form_valid(comment_form)
        
        return self.form_invalid(comment_form)
    
    def get_context_data(self):
        post = self.get_object()
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        #retrieving similar posts
        post_tags_ids = post.tags.values_list('id',flat=True)
        similar_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
        return {'post':post,'comments':comments,'comment_form':comment_form,'similar_posts':similar_post}
        
    def get_object(self):
        post = get_object_or_404(Post,
                                 slug = self.kwargs['slug'],
                                 status = 'published',
                                 publish__year = self.kwargs['year'],
                                 publish__month = self.kwargs['month'],
                                 publish__day = self.kwargs['day']
                                 )
        return post
    
    def form_valid(self,form):
        post = self.get_object()
        form.instance.post = post
        form.save()
        messages.success(self.request, 'comment added successfully!')
        return redirect(post.get_absolute_url())
    
    def form_invalid(self,form):
        context = self.get_context_data()
        context.update({'comment_form':form})
        messages.warning(self.request, 'comment not added!')
        return render(self.request,'detail.html',context=context)
    
class PostShare(FormView):
    form_class = EmailForm
    template_name = 'share.html'
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        post = self.get_object()
        
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
        messages.success(self.request, 'Post Shared Successfully!')
        return redirect('blog:post_share',self.kwargs['pk'])
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Post Not Shared!')
        return super().form_invalid(form)
    
    #called only at GET request
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context
    
    def get_object(self):
        post = get_object_or_404(Post,id=self.kwargs['pk'])
        return post
    
class SearchView(View):
    def get(self,request,*args,**kwargs):
        if 'query' in self.request.GET:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                form_data=form.cleaned_data
                return self.form_valid(form_data)
            return self.form_invalid(form)
        return render(self.request,'search.html',context={'form':SearchForm()})
    
    def form_valid(self,form):
        query = form['query']
        search_vector = SearchVector('title','body')
        search_query = SearchQuery(query)
        results = Post.published.annotate(
            search = search_vector,
            rank = SearchRank(search_vector,search_query)
        ).filter(search=search_query).order_by('-rank')
        return render(self.request,'search.html',context={'query':query,'results':results})
    
    def form_invalid(self,form):
        return render(self.request,'search.html',context={'form':form})