from django.urls import path

from . import views

urlpatterns = [
    path('',views.PostList.as_view(), name = 'all'),
    path('new/', views.CreatPost.as_view(),name='create'),
    path('by/<str:username>/',views.UserPosts.as_view(),name='for_user'),
    path('by/<str:username>/<int:pk>/',views.PostDetail.as_view(),name='single'),
    path('delete/<int:pk>',views.DeletePost.as_view(),name = 'delete'),
    
]
