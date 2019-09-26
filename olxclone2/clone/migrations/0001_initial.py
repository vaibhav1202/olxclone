# Generated by Django 2.1.7 on 2019-07-05 11:00

import clone.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=100)),
                ('s_pn', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^0?[6-9]{1}\\d{9}$')])),
                ('s_email', models.EmailField(max_length=254)),
                ('item_name', models.CharField(max_length=100)),
                ('s_description', models.TextField()),
                ('s_img', models.ImageField(upload_to='images\\', validators=[clone.models.validate_img])),
                ('s_price', models.IntegerField()),
                ('s_years', models.DateTimeField(auto_now_add=True)),
                ('s_area', models.CharField(max_length=100)),
            ],
        ),
    ]
