# Generated by Django 5.0.6 on 2024-07-17 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзину', 'verbose_name_plural': 'Корзина'},
        ),
    ]
