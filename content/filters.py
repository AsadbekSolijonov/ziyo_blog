from django_filters import FilterSet
import django_filters

from content.models import Blog


class BlogFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    created_at = django_filters.DateTimeFromToRangeFilter(field_name='created_at')
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = ['title', ]
