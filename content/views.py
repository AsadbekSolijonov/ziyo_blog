from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from datetime import datetime

from content.models import Blog
from content.serializers import BlogSerializer


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyListBlogView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Blog.objects.filter(user=self.request.user)
        return Blog.objects.all()


class BlogRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
