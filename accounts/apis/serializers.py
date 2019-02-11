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
        required=False,
        help_text="User id (optional)"
    )
    skill = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        help_text="String value"
    )
    rating = serializers.IntegerField(
        required=True,
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        help_text='rating from 0 to 100'
    )

    def create(self, validated_data):
        skill = SkillSet.objects.create(**validated_data)
        return skill

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.skill = validated_data.get('skill', instance.skill)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

    class Meta:
        model = SkillSet
        fields = ('skill', 'rating', 'user_id')

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=SkillSet.objects.all(),
        #         fields=('skill', 'user_id')
        #     )
        # ]


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


class ExperienceSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the experience model
    """
    def create(self, validated_data):
        experience = Experience.objects.create(**validated_data)
        return experience

    class Meta:
        model = Experience
        fields = '__all__'
