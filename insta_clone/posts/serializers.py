from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Story, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'image', 'caption', 'created_at', 'user', 'user_name', 'likes_count', 'profile_image']
        read_only_fields = ['user', 'user_name', 'created_at', 'likes_count', 'profile_image']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_profile_image(self, obj):
        profile, _ = Profile.objects.get_or_create(user=obj.user)
        request = self.context.get("request")
        if profile.profile_image:
            if request:
                return request.build_absolute_uri(profile.profile_image.url)
            return profile.profile_image.url
        return None


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'created_at', 'user', 'user_name', 'profile_image']
        read_only_fields = ['user', 'user_name', 'created_at', 'profile_image']

    def get_profile_image(self, obj):
        profile, _ = Profile.objects.get_or_create(user=obj.user)
        request = self.context.get("request")
        if profile.profile_image:
            if request:
                return request.build_absolute_uri(profile.profile_image.url)
            return profile.profile_image.url
        return None


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']
        read_only_fields = ['user']


class StorySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'image', 'created_at', 'user', 'user_name', 'profile_image']
        read_only_fields = ['user', 'user_name', 'created_at', 'profile_image']

    def get_profile_image(self, obj):
        profile, _ = Profile.objects.get_or_create(user=obj.user)
        request = self.context.get("request")
        if profile.profile_image:
            if request:
                return request.build_absolute_uri(profile.profile_image.url)
            return profile.profile_image.url
        return None


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_image']

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None


class UserSearchSerializer(serializers.ModelSerializer):
    bio = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_image']

    def get_bio(self, obj):
        profile, _ = Profile.objects.get_or_create(user=obj)
        return profile.bio

    def get_profile_image(self, obj):
        profile, _ = Profile.objects.get_or_create(user=obj)
        request = self.context.get("request")
        if profile.profile_image:
            if request:
                return request.build_absolute_uri(profile.profile_image.url)
            return profile.profile_image.url
        return None