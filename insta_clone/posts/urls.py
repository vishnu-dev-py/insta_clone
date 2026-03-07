from django.urls import path

from .views import (
    home,
    register_page,
    login_page,
    logout_user,
    RegisterUser,
    PostListCreateView,
    StoryListCreateView,
    toggle_like,
    CommentListCreateView,
    delete_comment,
    UserSearchView,
    MyProfileView,
    MyProfileUpdateView,
    UserProfileView,
)

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', logout_user, name="logout"),

    path('api/register/', RegisterUser.as_view()),
    path('api/posts/', PostListCreateView.as_view()),
    path('api/stories/', StoryListCreateView.as_view()),
    path('api/like/', toggle_like),
    path('api/comments/', CommentListCreateView.as_view()),
    path('api/comments/delete/<int:id>/', delete_comment),

    path('api/search-users/', UserSearchView.as_view()),
    path('api/my-profile/', MyProfileView.as_view()),
    path('api/my-profile/update/', MyProfileUpdateView.as_view()),
    path('api/users/<int:user_id>/profile/', UserProfileView.as_view()),
]