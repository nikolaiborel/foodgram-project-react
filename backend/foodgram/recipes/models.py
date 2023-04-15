from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'name: {self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название')
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет в HEX',
        validators=[RegexValidator(
            regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
            message='Введенное значение не является HEX форматом'
        )]

    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальный слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'name: {self.name}'


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Название рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты рецепта',
        related_name='ingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов',
        related_name='tags'
    )
    image = models.ImageField(
        upload_to='recipes/images',
        verbose_name='Изображение',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1, message='Минимальное значение 1!')]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'name: {self.name}'


class AmountIngredientsInRecipes(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='рецепт',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        validators=[MinValueValidator(1, message='Минимальное значение 1!')]
    )

    def __str__(self):
        return f'name: {self.ingredient.name},' \
               f' {self.ingredient.measurement_unit}, {self.amount}'


class Carts(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='in_carts'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Список рецептов',
        related_name='in_carts'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        ordering = ('-pub_date',)
        constraints = UniqueConstraint(
            fields=['user', 'recipes'],
            name='unique_list_recipes'
        ),

    def __str__(self):
        return f'{self.user} добавил "{self.recipes}" в корзину'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='favorites'
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Список избранных рецептов',
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное',
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} добавил в избранное "{self.recipes}"'
