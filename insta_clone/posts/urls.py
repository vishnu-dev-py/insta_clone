from django.urls import path
from .views import (
    home,
    RegisterUser,
    PostListCreateView,
    StoryListCreateView,
    toggle_like,
    CommentListCreateView,
    CommentDeleteView
)

urlpatterns = [
    path('', home),
    path('api/register/', RegisterUser.as_view()),
    path('api/posts/', PostListCreateView.as_view()),
    path('api/stories/', StoryListCreateView.as_view()),
    path('api/like/', toggle_like),
    path('api/comments/', CommentListCreateView.as_view()),
    path('api/comments/delete/<int:pk>/', CommentDeleteView.as_view()),
]