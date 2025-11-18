from django.contrib.auth.models import User
from rest_framework import serializers

from content.models import Tag, Comment, Blog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'created_at']


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'body', 'user', 'image', 'created_at', 'updated_at', 'views', 'like_count',
                  'is_published']
        read_only_fields = ('id', 'views', 'created_at', 'updated_at')
