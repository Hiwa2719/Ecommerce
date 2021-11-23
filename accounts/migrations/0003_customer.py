# Generated by Django 3.2.9 on 2021-11-22 18:53

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.user')),
                ('verified_email', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.user',),
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]