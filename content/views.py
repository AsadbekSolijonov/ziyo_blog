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

    def get_queryset(self):
        return Comment.objects.filter(blog_id=self.kwargs['blog_pk']).select_related('user', 'blog')

    def perform_create(self, serializer):
        blog_id = self.kwargs['blog_pk']
        serializer.save(user=self.request.user, blog_id=blog_id)


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    # get_queryset published blogs.

    @action(detail=False, methods=['GET', ], url_path='me_blogs')
    def my_blogs(self, *args, **kwargs):
        blogs = Blog.objects.filter(user=self.request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    # unpublished blogs action
