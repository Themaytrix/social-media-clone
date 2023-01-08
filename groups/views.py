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
            # create a member of object(user) if user is now hoining group
            GroupMember.objects.create(user=self.request.user,group=group)
        except :
            messages.warning(self.request,"Already a member!!")
        else:
            messages.success(self.request,"Joined group")
            
        return super().get(request,*args,**kwargs)
    
    

class LeaveGroup(LoginRequiredMixin,RedirectView):
    # getting the url to redirect to
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,"sorry you are not in this group")
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')
        return super().get(request,*args,**kwargs)