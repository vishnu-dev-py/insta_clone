from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta

from .models import Post, Like, Comment, Story, Profile
from .serializers import (
    UserSerializer,
    PostSerializer,
    CommentSerializer,
    StorySerializer,
    UserSearchSerializer,
)


def home(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    return render(request, "posts/index.html", {"username": request.user.username})


def register_page(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if username == "" or password == "":
            error = "Please enter username and password."
            return render(request, "posts/register.html", {"error": error})

        if User.objects.filter(username=username).exists():
            error = "Username already exists."
            return render(request, "posts/register.html", {"error": error})

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.get_or_create(user=user)

        return redirect("/login/")

    return render(request, "posts/register.html", {"error": error})


def login_page(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if username == "" or password == "":
            error = "Please enter username and password."
            return render(request, "posts/login.html", {"error": error})

        user = authenticate(request, username=username, password=password)

        if user is None:
            error = "Invalid username or password."
            return render(request, "posts/login.html", {"error": error})

        login(request, user)
        return redirect("/")

    return render(request, "posts/login.html", {"error": error})


def logout_user(request):
    logout(request)
    return redirect("/login/")


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoryListCreateView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        last_24 = timezone.now() - timedelta(hours=24)
        return Story.objects.filter(created_at__gte=last_24).order_by("-created_at")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
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
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["DELETE"])
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
        query = (request.GET.get("q") or "").strip()

        users = User.objects.exclude(id=request.user.id)
        if query:
            users = users.filter(username__icontains=query)

        serializer = UserSearchSerializer(users[:20], many=True, context={"request": request})
        return Response(serializer.data)


class MyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        posts = Post.objects.filter(user=request.user).order_by("-created_at")

        profile_image = None
        if profile.profile_image:
            profile_image = request.build_absolute_uri(profile.profile_image.url)

        return Response({
            "username": request.user.username,
            "bio": profile.bio,
            "profile_image": profile_image,
            "posts": PostSerializer(posts, many=True, context={"request": request}).data
        })


class MyProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.bio = request.data.get("bio", "")
        profile.save()
        return Response({"message": "Profile updated"})


class ProfileImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        if "profile_image" not in request.FILES:
            return Response({"error": "No profile image provided"}, status=status.HTTP_400_BAD_REQUEST)

        profile.profile_image = request.FILES["profile_image"]
        profile.save()

        return Response({
            "message": "Profile image uploaded successfully",
            "profile_image": request.build_absolute_uri(profile.profile_image.url)
        })


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        profile, _ = Profile.objects.get_or_create(user=user)
        posts = Post.objects.filter(user=user).order_by("-created_at")

        profile_image = None
        if profile.profile_image:
            profile_image = request.build_absolute_uri(profile.profile_image.url)

        return Response({
            "username": user.username,
            "bio": profile.bio,
            "profile_image": profile_image,
            "posts": PostSerializer(posts, many=True, context={"request": request}).data
        })