from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from blog.models import Post, Comment, Reply
from notifications.models import Notification

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    user_id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255, required=False)
    success = serializers.BooleanField(default=False)


# Custom Validator for password.
def password_validate(password):
    """
    Validate Password.
    """
    if not password:
        raise serializers.ValidationError(
            {'password': 'Password cannot be empty!'}
        )
    elif len(password) < 8:
        raise serializers.ValidationError(
            {'password': 'Password too short.'}
        )


class RegisterSerializer(serializers.ModelSerializer):

    user_check = UniqueValidator(
        queryset=User.objects.all(),
        message='username already exists'
    )
    email_check = UniqueValidator(
        queryset=User.objects.all(),
        message='Email already exists'
    )
    first_name = serializers.CharField(
        max_length=255,
        help_text='String contains the first name'
    )
    last_name = serializers.CharField(
        max_length=255,
        help_text='String contains the last name'
    )
    email = serializers.EmailField(
        required=True,
        max_length=100,
        validators=[email_check],
        help_text='A unique email'
    )
    username = serializers.CharField(
        required=True,
        validators=[user_check],
        help_text='A unique string which identifies user'
    )
    password = serializers.CharField(
        min_length=8,
        validators=[password_validate],
        help_text='Password having greater than 8 character'
    )
    is_editor = serializers.BooleanField(
        default=False,
        help_text='Boolean value for editor'
    )
    # is_chief = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'first_name', 'last_name', 'is_editor')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        help_text='A unique string which identifies user'
    )
    password = serializers.CharField(
        max_length=100,
        write_only=True,
        validators=[password_validate],
        help_text='Password having greater than 8 character'
    )


class PostApprovalFormSerializer(serializers.ModelSerializer):
    is_approve = serializers.BooleanField(help_text="Boolean value")

    class Meta:
        model = Post
        fields = ('is_approve',)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class BlogCreateSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        max_length=255,
        trim_whitespace=True,
        help_text="Title of blog"
    )
    text = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        help_text="Text/Content of blog"
    )
    owner_id = serializers.ModelField(
        model_field=User()._meta.get_field('id'),
        required=False,
        help_text="UserId of current user. (optional)"
    )
    request_from = serializers.CharField(
        max_length=10,
        default='api',
        read_only=True
    )

    def create(self, validated_data):
        validated_data['request_from'] = 'api'
        post = Post.objects.create(**validated_data)
        return post

    class Meta:
        model = Post
        fields = ('title', 'text', 'owner_id', 'request_from')


class CommentSerializer(serializers.ModelSerializer):

    comment = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        help_text="String value"
    )
    blog_id = serializers.ModelField(
        model_field=Post()._meta.get_field('id'),
        help_text="blog Id on which comment will apply"
    )
    user_id = serializers.ModelField(
        model_field=User()._meta.get_field('id'),
        read_only=True
    )

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    class Meta:
        model = Comment
        fields = ('comment', 'blog_id', 'user_id')


class ReplySerializer(serializers.ModelSerializer):

    reply = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        help_text="String value"
    )
    which_comment_id = serializers.ModelField(
        model_field=Comment()._meta.get_field('id'),
        help_text="CommentID on which user reply "
    )
    blog_id = serializers.ModelField(
        model_field=Post()._meta.get_field('id'),
        help_text="blog Id on which reply will apply"
    )
    user_id = serializers.ModelField(
        model_field=User()._meta.get_field('id'),
        read_only=True
    )

    def create(self, validated_data):
        reply = Reply.objects.create(**validated_data)
        return reply

    class Meta:
        model = Reply
        fields = ('reply', 'which_comment_id', 'blog_id', 'user_id')


class NotificationSerializer(serializers.ModelSerializer):

    unread = serializers.BooleanField(
        default=False,
        help_text="Boolean value for read status"
    )

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('verb', 'object_id', 'description',
                            'deleted', 'sender', 'content_type', 'blog')
