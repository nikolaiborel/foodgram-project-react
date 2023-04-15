from rest_framework.routers import DefaultRouter
from .views import RecipesViewSet, IngredientsViewSet, TagViewSet
from django.urls import include, path

router = DefaultRouter()

router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
