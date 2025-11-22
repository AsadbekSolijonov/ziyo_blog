from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import F

from content.filters import BlogFilter
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BlogFilter
    search_fields = ('title', 'user__username')

    def get_queryset(self):
        qs = Blog.objects.all()
        if self.action == 'my_blogs':
            qs = qs.filter(user=self.request.user)
        elif self.action == 'unpublished':
            qs = qs.filter(is_published=False, user=self.request.user)
        return qs

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        Blog.objects.filter(id=obj.id).update(views=F('views') + 1)
        obj.refresh_from_db(fields=['views'])
        serializer = BlogSerializer(obj)
        return Response(serializer.data)

    @action(detail=False, methods=['get', ], url_path='me_blogs')
    def my_blogs(self, *args, **kwargs):
        blogs = self.get_queryset()
        page = self.paginate_queryset(blogs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get', ], url_path="Unpublished")
    def unpublished(self, *args, **kwargs):
        unp_blogs = self.get_queryset()
        page = self.paginate_queryset(unp_blogs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BlogSerializer(unp_blogs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', ], permission_classes=[IsAuthenticated, ])
    def like(self, requst, pk=None):
        obj = self.get_object()
        obj.likes.add(self.request.user)
        return Response({"detial": "Successfully is liked."})

    @action(detail=True, methods=['post', ], permission_classes=[IsAuthenticated, ])
    def unlike(self, requst, pk=None):
        obj = self.get_object()
        obj.likes.remove(self.request.user)
        return Response({"detial": "Successfully is unliked."})
