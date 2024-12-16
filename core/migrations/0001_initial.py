# Generated by Django 5.1.4 on 2024-12-16 11:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=150, verbose_name='Nome do arquivo')),
                ('resume', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(3000)], verbose_name='Resumo feito')),
                ('is_resumed', models.BooleanField(default=False, verbose_name='Esse pdf ja foi resumido?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
            ],
        ),
    ]