from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView
from django.http import Http404
from django.contrib import messages
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from braces.views import SelectRelatedMixin
from .models import Post,Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class PostList(SelectRelatedMixin,ListView):
    model = Post
    select_related = ('user','group')
    

    
    
class UserPosts(ListView):
    model = Post
    template_name = 'posts/user_post_list.html'
    
    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact =self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context
    
class PostDetail(SelectRelatedMixin,DetailView):
    model = Post
    select_related = ('user','group')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact = self.kwargs.get('username'))
    
    def get_context_data(self, **kwargs):
        posts = Post.objects.get(id=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        print(posts)
        context['comments'] = posts.comment.all()
        return context
    

class CreatPost(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    fields = ('message','group')
    model = Post
    
    # validate form
    def form_valid(self,form):
        
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        print(self.object)
        return super().form_valid(form)
    

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,DeleteView):
    model = Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
    
class CommentList(ListView,SelectRelatedMixin):
    model = Post
    select_relate = ('post','comment')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post,id='pk')
        context['post_comments'] = post.comment.all()
        return context
    
    
    
    
@login_required
def create_comment(request):
    post = get_object_or_404(Post)
    comments = post.comment.all()
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance = form.save(commit=False)
            form.instance.user = post.user
            form.instance.post_id = post.pk
            form.post = post
            form.save()
            # username = post.user.get_username()
            return redirect(post)
    else:
        form = CommentForm()
            
    return render(request,'posts/comment_form.html',{
        'form': form,
        'comments' : comments,
        'posts': post
    })
            