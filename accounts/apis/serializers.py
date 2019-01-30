from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import *


User = get_user_model()


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    user_id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255, required=False)
    success = serializers.BooleanField(default=False)


class SkillSerializer(serializers.Serializer):
    """
    This serializer serializes the skill model
    """
    user_id = serializers.ModelField(
        model_field=User()._meta.get_field('id'),
        read_only=True
    )
    skill = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        help_text="String value"
    )
    rating = serializers.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )

    def create(self, validated_data):
        print(validated_data)
        skill = SkillSet.objects.create(**validated_data)
        return skill

    class Meta:
        model = SkillSet
        fields = ('user', 'skill', 'rating')
