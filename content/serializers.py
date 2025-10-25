from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from content.models import Blog
from content.validators import is_not_con_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']


class BlogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # user = serializers.StringRelatedField()
    content = serializers.CharField(source='body')
    title_len = serializers.IntegerField(source='title_length', read_only=True)
    content_len = serializers.IntegerField(source='body_length', read_only=True)
    content_title_diff = serializers.SerializerMethodField()  # read_only

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'user', 'title_len', 'content_len', 'content_title_diff']
        read_only_fields = ('id', 'user', 'content_title_diff')

    # field-level validation
    def validate_title(self, value):
        if 'con' in value:
            raise serializers.ValidationError("Iltimos con so'zini ishlatmang!")
        return value

    # object-level validation.
    def validate(self, attrs):
        if attrs.get('title'):
            if attrs['title'].lower() == attrs['body'].lower():
                raise serializers.ValidationError("title va body maydonlar teng bo'lishi mumkin emas.")
        return attrs

    # def to_internal_value(self, data):
    #     resource_data = data['resource']
    #     return super().to_internal_value(resource_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        from datetime import datetime
        rep['now'] = datetime.now()
        rep['hello'] = self.context.get('request')
        return rep

    def get_content_title_diff(self, obj):
        diff = obj.body_length / obj.title_length
        if diff == 1:
            return F"Content va Title teng"
        elif 0 <= diff <= 1:
            diff = obj.title_length / obj.body_length
            return f"Title, Contentdan {diff:,.2f} marta ko'p"
        return f"Content qismi, title qismidan {diff:,.2f} marta ko'p."
