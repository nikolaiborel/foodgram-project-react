# Generated by Django 4.1.7 on 2023-04-02 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfoodgram',
            name='password',
            field=models.CharField(max_length=150, verbose_name='password'),
        ),
    ]