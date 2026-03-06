from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import Post, Like, Comment, Story
from .serializers import (
    UserSerializer,
    PostSerializer,
    CommentSerializer,
    StorySerializer
)


def home(request):
    return render(request, 'posts/index.html')


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = User.objects.first()
        serializer.save(user=user)


class StoryListCreateView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        last_24 = timezone.now() - timedelta(hours=24)
        return Story.objects.filter(created_at__gte=last_24).order_by('-created_at')

    def perform_create(self, serializer):
        user = User.objects.first()
        serializer.save(user=user)


@api_view(['POST'])
def toggle_like(request):
    user = User.objects.first()
    post_id = request.data.get("post")

    post = Post.objects.get(id=post_id)

    like = Like.objects.filter(user=user, post=post)

    if like.exists():
        like.delete()
        return Response({"message": "unliked"})

    Like.objects.create(user=user, post=post)
    return Response({"message": "liked"})


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = User.objects.first()
        serializer.save(user=user)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]