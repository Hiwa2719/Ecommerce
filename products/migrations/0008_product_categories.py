# Generated by Django 3.2.9 on 2021-11-05 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='products.Category'),
        ),
    ]
