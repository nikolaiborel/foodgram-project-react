from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status

from recipes.models import (Ingredient, Recipes,
                            Tag, Favorite,
                            AmountIngredientsInRecipes,
                            Carts)
from .serializers import (IngredientSerializer, TagSerializer,
                          ReadRecipesSerializer, WriteRecipeSerializer,
                          ImageRecipesSerializer)
from .permissions import OwnerOrAdminOrReadOnly
from .filters import IngredientFilter, RecipesFilter


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    permission_classes = (OwnerOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == SAFE_METHODS:
            return ReadRecipesSerializer
        return WriteRecipeSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favorite, request.user, pk)
        else:
            return self.delete_from(Carts, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Carts, request.user, pk)
        else:
            return self.delete_from(Carts, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipes__id=pk).exists():
            return Response({
                'errors': 'Рецепт уже добавлен'},
                status=status.HTTP_400_BAD_REQUEST)
        recipes = get_object_or_404(Recipes, id=pk)
        model.objects.create(user=user, recipes=recipes)
        serializer = ImageRecipesSerializer(recipes)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipes__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Такого рецепта не существует'},
            status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated, ]
    )
    def download_cart(self, request):
        user = request.user
        if not user.in_carts.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = AmountIngredientsInRecipes.objects.filter(
            recipe__in_carts=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        today = datetime.today()
        shopping_list = (f'Список покупок для {user.get_full_name()} \n\n',
                         f'data: {today: %Y-%m-%d} \n\n')
        shopping_list += '\n'.join([
            f'{ingredient["ingredient__name"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
            f'{ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_list += f'\n\n foodgram({today: %Y})'
        file_name = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
