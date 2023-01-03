from django.db import models
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
from django import template
# returning the user model currently active

User = get_user_model()
# registering custom template tags
register = template.Library()




# Create your models here.
class Group(models.Model):
    pass

class GroupMembers(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='membership')
    user = models.ForeignKey(related_name='')
    
