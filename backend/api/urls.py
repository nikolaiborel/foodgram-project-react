from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import RecipesViewSet, IngredientsViewSet, TagViewSet

router = DefaultRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
