from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from .models import Group,GroupMember

# Create your views here.

class CreateGroup(LoginRequiredMixin,CreateView):
    fields= ('name','description')
    model = Group