from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from content import views
from content.views import TagViewSet, CommentViewSet, BlogViewSet

router = DefaultRouter()
router.register("blogs", BlogViewSet, basename='blog')
router.register("tags", TagViewSet, basename='tag')

blog_router = NestedSimpleRouter(router, "blogs", lookup='blog')
blog_router.register("comments", CommentViewSet, basename='blog-comment')

urlpatterns = [
    path('', include(blog_router.urls))
]

urlpatterns += router.urls
