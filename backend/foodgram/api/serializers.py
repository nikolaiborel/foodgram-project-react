from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from drf_extra_fields.fields import Base64ImageField
from django.db.models import F
from recipes.models import Ingredient, Tag, Recipes, AmountIngredientsInRecipes
import logging

User = get_user_model()


class UserSerializerCre(UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS)+(User.USERNAME_FIELD, 'password')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReadRecipesSerializer(ModelSerializer):
    ingredients = SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorite = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorite', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        recipes = obj
        ingredients = recipes.ingredients.values(
            'id',
            'name',
            amount=F('amountingredientsinrecipes__amount')
        )
        return ingredients

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipes=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.in_carts.filter(recipes=obj).exists()


class WriteIngredientsSerializer(ModelSerializer):
    id = IntegerField(write_only=True)
    amount = IntegerField(write_only=True)

    class Meta:
        model = AmountIngredientsInRecipes
        fields = ('id', 'amount')


class WriteRecipeSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = WriteIngredientsSerializer(many=True)

    class Meta:
        model = Recipes
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'author'
        )

    def validate(self, data):
        ingredients = data['ingredients']
        tags = data['tags']
        if not ingredients:
            raise ValidationError({
                'ingredients': 'Укажите минимум 1 ингредиент'
            })
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError({
                    'ingredients': 'Ингредиенты не должны повторяться'
                })
            if int(item['amount']) <= 0:
                raise ValidationError({
                    'amount': 'Количество должно быть больше 0'
                })
            ingredients_list.append(ingredient)
        if not tags:
            raise ValidationError({'tags': 'Укажите минимум один тег'})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({'tags': 'Теги должны быть уникальными'})
            tags_list.append(tag)
        return data

    @transaction.atomic
    def create_ingredients_amount(self, ingredients, recipes):
        AmountIngredientsInRecipes.objects.bulk_create(
            [AmountIngredientsInRecipes(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipes, amount=ingredient['amount']
            ) for ingredient in ingredients])

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipes = Recipes.objects.create(**validated_data)
        recipes.tags.set(tags)
        self.create_ingredients_amount(
            recipes=recipes,
            ingredients=ingredients
        )
        return recipes

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amount(
            recipes=instance,
            ingredients=ingredients
        )
        super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ReadRecipesSerializer(instance, context=context).data


class ImageRecipesSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
