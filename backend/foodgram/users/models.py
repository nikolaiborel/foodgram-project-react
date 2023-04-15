from django.contrib.auth.models import AbstractUser
from django.db import models


class UserFoodgram(AbstractUser):
    password = models.CharField("password", max_length=150)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.get_full_name()


class Subscribe(models.Model):
    user = models.ForeignKey(UserFoodgram,
                             on_delete=models.CASCADE,
                             related_name='subscribed_to',
                             verbose_name='Подписчик')
    author = models.ForeignKey(UserFoodgram,
                               on_delete=models.CASCADE,
                               related_name='subscribed_by',
                               verbose_name='Автор',
                               )

    class Meta:
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'
        ordering = ('author_id',)

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
