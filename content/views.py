from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from content.models import Blog
from content.serializers import BlogSerializer


@api_view(['GET', 'POST'])
def blogs(request):
    if request.method == 'GET':
        blogs_ = Blog.objects.all()
        serializer = BlogSerializer(blogs_, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data, context={"request": request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
