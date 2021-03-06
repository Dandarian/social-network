from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view()),
    path('auth/', views.Login.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view()),
    path('analytics/', views.AnalyticsList.as_view()),
    path('user-activity/', views.UserActivityList.as_view()),
    path('user-activity/<int:pk>/', views.UserActivityDetail.as_view()),
]

# Formats endings, for example .json
urlpatterns = format_suffix_patterns(urlpatterns)
