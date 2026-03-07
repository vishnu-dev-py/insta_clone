from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from .models import Post, Like, Comment, Story, Profile
from .serializers import (
    UserSerializer,
    PostSerializer,
    CommentSerializer,
    StorySerializer,
    ProfileSerializer,
    UserSearchSerializer,
)


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "posts/index.html", {"username": request.user.username})


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "posts/register.html", {"error": "Username and password are required"})

        if User.objects.filter(username=username).exists():
            return render(request, "posts/register.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.get_or_create(user=user)

        return redirect("login")

    return render(request, "posts/register.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "posts/login.html", {"error": "Invalid username or password"})

    return render(request, "posts/login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoryListCreateView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        last_24 = timezone.now() - timedelta(hours=24)
        return Story.objects.filter(created_at__gte=last_24).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request):
    user = request.user
    post_id = request.data.get("post")

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    like = Like.objects.filter(user=user, post=post)

    if like.exists():
        like.delete()
        return Response({"message": "unliked"})

    Like.objects.create(user=user, post=post)
    return Response({"message": "liked"})


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    if comment.user != request.user:
        return Response({"error": "You can delete only your own comment"}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({"message": "deleted"})


class UserSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get("q", "").strip()

        users = User.objects.exclude(id=request.user.id)
        if query:
            users = users.filter(username__icontains=query)

        serializer = UserSearchSerializer(users[:20], many=True)
        return Response(serializer.data)


class MyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        posts = Post.objects.filter(user=request.user).order_by('-created_at')

        return Response({
            "username": request.user.username,
            "bio": profile.bio,
            "posts": PostSerializer(posts, many=True, context={"request": request}).data
        })


class MyProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        bio = request.data.get("bio", "")
        profile.bio = bio
        profile.save()
        return Response({"message": "Profile updated"})


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        profile, _ = Profile.objects.get_or_create(user=user)
        posts = Post.objects.filter(user=user).order_by('-created_at')

        return Response({
            "username": user.username,
            "bio": profile.bio,
            "posts": PostSerializer(posts, many=True, context={"request": request}).data
        })