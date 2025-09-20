from rest_framework import serializers
from content.models import Blog
from content.validators import is_not_con_validator


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    content = serializers.CharField(source='body')
    title_len = serializers.IntegerField(source='title_length', read_only=True)
    content_len = serializers.IntegerField(source='body_len', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'user', 'title_len', 'content_len']
        read_only_fields = ('id', 'user')

    # field-level validation
    def validate_title(self, value):
        if 'con' in value:
            raise serializers.ValidationError("Iltimos con so'zini ishlatmang!")
        return value

    # object-level validation.
    def validate(self, attrs):
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
