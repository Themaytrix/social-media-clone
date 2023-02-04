from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.PostList.as_view(), name = 'all'),
    path('new/', views.CreatPost.as_view(),name='create'),
    path('by/<slug:username>/',views.UserPosts.as_view(),name='for_user'),
    path('by/<slug:username>/<int:pk>/',views.PostDetail.as_view(),name='single'),
    path('delete/<int:pk>',views.DeletePost.as_view(),name = 'delete'),
    path('comment/',views.create_comment,name='comment'),
    path('comment/<slug:username>/<int:pk>',views.CommentList.as_view(), name='comment_list'),
    
    
]
