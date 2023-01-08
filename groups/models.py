from django.db import models
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
from django import template
from django.urls import reverse
# returning the user model currently active

User = get_user_model()
# registering custom template tags
register = template.Library()




# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User,through='GroupMember')
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)
    
    # redirect onto created group
    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ['name']
    
    
class GroupMember(models.Model):
    # getting the group the user is in
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='membership')
    # getting the list of groups member is in
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        unique_together = ('group','user')
    
    
