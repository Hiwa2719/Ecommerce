# Generated by Django 3.2.9 on 2021-11-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_product_features'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('name',), name='unique name'),
        ),
    ]
