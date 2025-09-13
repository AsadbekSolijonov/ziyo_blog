from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from content.models import Blog
from content.serializers import BlogSerializer, BlogFSerializer


@api_view(['GET'])
def hello_world(request):
    return Response({
        "message": "Hello world!",
        "status": 200,
        "datetime": datetime.now().isoformat()
    })


@api_view(['GET'])  # HTTP METHODS = GET, POST, PUT, PATCH, DELETE
def welcome(request):
    return Response({
        "message": "Xush kelibsiz, Mehmon"
    })


@api_view(['GET', 'POST'])
def blogs(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def fblogs(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogFSerializer(blogs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogFSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
