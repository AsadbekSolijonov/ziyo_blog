from rest_framework import serializers


def is_not_con_validator(value):
    if 'con' in value:
        raise serializers.ValidationError("Ilitmos con bo'lmasin.")
    return value
