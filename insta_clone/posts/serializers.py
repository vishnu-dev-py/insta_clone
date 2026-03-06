from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Story


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'image', 'caption', 'created_at', 'user', 'user_name', 'likes_count']
        read_only_fields = ['user', 'user_name', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'created_at', 'user', 'user_name']
        read_only_fields = ['user', 'user_name', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']
        read_only_fields = ['user']


class StorySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'image', 'created_at', 'user', 'user_name']
        read_only_fields = ['user', 'user_name', 'created_at']