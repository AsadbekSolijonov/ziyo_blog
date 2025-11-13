from rest_framework.permissions import IsAuthenticated
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

