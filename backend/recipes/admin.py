from django.contrib import admin
from django.contrib.admin import display

from .models import (Ingredient,
                     Tag,
                     Recipes,
                     AmountIngredientsInRecipes,
                     Favorite,
                     Carts
                     )


@admin.register(Recipes)
class AdminRecipes(admin.ModelAdmin):
    list_display = ('name', 'pk', 'author', 'pub_date')
    readonly_fields = ('favorites', )
    list_filter = ('author', 'name', 'tags')

    @display(description='Кол-во в избранных')
    def favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class AdminIngredients(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', )


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Carts)
class AdminCarts(admin.ModelAdmin):
    list_display = ('user', 'recipes', 'pub_date')


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = ('user', 'recipes', )


@admin.register(AmountIngredientsInRecipes)
class AdminAmountIngredientsInRecipes(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
