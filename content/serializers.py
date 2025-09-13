from rest_framework import serializers
from content.models import Blog
from content.validators import is_not_con_validator


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'body']

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


class BlogFSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[is_not_con_validator, ], required=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'body']
