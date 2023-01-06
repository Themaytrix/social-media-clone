from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView,DetailView,RedirectView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from .models import Group,GroupMember
from django.contrib import messages

# Create your views here.

class CreateGroup(LoginRequiredMixin,CreateView):
    fields= ('name','description')
    model = Group
    
class SingleGroup(DetailView):
    model = Group

class ListGroup(ListView):
    model = Group
    
class JoinGroup(LoginRequiredMixin,RedirectView):
    # getting the url to redirect to
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    
    # checking if user is already a member of group
    def get(self,request,*args,**kwargs):
        # get the group onject at slug url
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except :
            messages.warning()

class LeaveGroup():
    pass