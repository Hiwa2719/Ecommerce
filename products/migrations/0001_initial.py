# Generated by Django 3.2.9 on 2021-11-04 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField()),
                ('is_active', models.BooleanField(default=True, help_text='Instead of deleting a product just make it de-active from here', verbose_name='active')),
                ('is_digital', models.BooleanField(default=False, help_text='Designated whether a product is a digital product', verbose_name='digital status')),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
