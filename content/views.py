from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from datetime import datetime

from content.models import Blog
from content.serializers import BlogSerializer


# Function Based Views (FBV)  #CRUD - Create, Read, Update, Delete
@api_view(['GET', 'POST'])
def blogs(request):
    if request.method == 'GET':  # List
        blogs_ = Blog.objects.all()
        serializer = BlogSerializer(blogs_, many=True, context={"request": request})
        return Response(serializer.data)

    elif request.method == 'POST':  # Create
        serializer = BlogSerializer(data=request.data, context={"request": request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET', 'PATCH', 'DELETE'])  # pk - id
def single_blog(request, pk):
    blog = get_object_or_404(Blog, id=pk)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    # if request.method == 'PUT':
    #     serializer = BlogSerializer(blog, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)
    #     return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    # paritail Update

    if request.method == 'DELETE':
        blog.delete()
        return Response(status=204)


class BlogRetrieveUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
