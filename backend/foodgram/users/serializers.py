from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from .models import Subscribe
from djoser.serializers import UserCreateSerializer, UserSerializer

from recipes.models import Recipes

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    """
    Сериалзиатор регистрации пользователей (используется в сеттингс)
    """
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializerCustom(UserSerializer):
    """
    Кастомный пользовательский сериализатор
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=request.user, author=obj).exists()

    def to_representation(self, instance):
        if not self.context['request'].user.is_authenticated:
            return {"detail": "Учетные данные не были предоставлены."}
        return super().to_representation(instance)


class RecipeShortSerializer(serializers.ModelSerializer):
    """
    Мини-сериализатор рецептов
    """
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowList(serializers.ModelSerializer):
    '''Список подписчиков'''
    recipes = RecipeShortSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_subscribe', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribe(self, user):
        request = self.context.get('REQUEST')
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filters(user=user, author=request.user).exists()


class AuthSerializer(serializers.Serializer):
    '''Сериализатор аутентификации'''
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(label=('Password',), style={'input_type': 'password'})

    def validate(self, atr):
        email = atr.get('email')
        password = atr.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Неверные данные', code='authorization')
        else:
            raise serializers.ValidationError('Все поля должны быть заполнены', code='authorization')
        atr['user'] = user
        return atr


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор подписки на пользователя
    """

    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('author', 'user'),
                message='Вы уже подписаны на автора',
            )
        ]

    @action(detail=True, methods=['POST'])
    def check_follow_myself(self, data):
        if data['user'] == data['follow']:
            raise serializers.ValidationError('Нельзя подписаться на самого себя')
        return data


