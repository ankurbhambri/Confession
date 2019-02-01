from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
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


class SkillSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the skill model
    # """
    user_id = serializers.ModelField(
        model_field=User()._meta.get_field('id'),
        required=False
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
        skill = SkillSet.objects.create(**validated_data)
        return skill

    class Meta:
        model = SkillSet
        fields = ('skill', 'rating', 'user_id')

        validators = [
            UniqueTogetherValidator(
                queryset=SkillSet.objects.all(),
                fields=('skill', 'user_id')
            )
        ]


class QualificationSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the qualification model
    """
    def create(self, validated_data):
        qualification = Qualification.objects.create(**validated_data)
        return qualification

    class Meta:
        model = Qualification
        fields = '__all__'
