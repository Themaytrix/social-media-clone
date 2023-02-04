from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from django.utils import timezone

from groups.models import Group
from django.contrib.auth import get_user_model

# getting active user model
User = get_user_model()

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.message
    
    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)
        
    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username": self.user.username,'pk':self.pk})
        
    class Meta:
        ordering = ['-created_at']
        unique_together =['user','message']
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    comment_text = models.TextField()
    comment_html = models.TextField(editable=False)
    post= models.ForeignKey(Post,related_name='comment',on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.comment_html
    
    def save(self,*args,**kwargs):
        self.comment_html = misaka.html(self.comment_text)
        # self.post_id = Comment.post.
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse("posts:single", kwargs={
            "username":self.user.username,
            "pk": self.post.pk,
            })
    
    
    
    class Meta:
        # creating a unique id for post and comment_text
        unique_together = ['post','comment_text']