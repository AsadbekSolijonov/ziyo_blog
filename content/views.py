from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from content.models import Tag, Comment, Blog
from content.serializers import TagSerializer, CommentSerializer, BlogSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, ]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    lookup_field = 'pk'
    lookup_url_kwarg = 'comment_pk'

    def get_queryset(self):
        blog_pk = self.kwargs.get('blog_pk')
        if blog_pk:
            return Comment.objects.filter(blog_id=blog_pk).select_related('user', 'blog')

    def perform_create(self, serializer):
        blog_pk = self.kwargs.get('blog_pk')
        serializer.save(user=self.request.user, blog_id=blog_pk)


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views += 1
        obj.save(update_fields=['views'])
        serializer = BlogSerializer(obj)
        return Response(serializer.data)

    @action(detail=False, methods=['GET', ], url_path='me_blogs')
    def my_blogs(self, *args, **kwargs):
        blogs = Blog.objects.filter(user=self.request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET', ], url_path="Unpublished")
    def unpublished(self, *args, **kwargs):
        unp_blogs = self.get_queryset().filter(is_published=False, user=self.request.user)
        serializer = BlogSerializer(unp_blogs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST', ], permission_classes=[IsAuthenticated, ])
    def like(self, requst, pk=None):
        obj = self.get_object()
        obj.likes.add(self.request.user)
        # obj.save(update_fields=['likes'])
        return Response({"detial": "Successfully is liked."})

    @action(detail=True, methods=['POST', ], permission_classes=[IsAuthenticated, ])
    def unlike(self, requst, pk=None):
        obj = self.get_object()
        obj.likes.remove(self.request.user)
        return Response({"detial": "Successfully is unliked."})
