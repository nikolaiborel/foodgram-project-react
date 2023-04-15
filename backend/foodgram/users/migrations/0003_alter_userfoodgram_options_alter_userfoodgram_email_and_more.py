# Generated by Django 4.1.7 on 2023-04-11 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userfoodgram_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfoodgram',
            options={'ordering': ('username',), 'verbose_name': ('Пользователь',), 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='userfoodgram',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='userfoodgram',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='userfoodgram',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last name'),
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcribed_by', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcribed_to', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'ordering': ('author_id',),
            },
        ),
    ]
