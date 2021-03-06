# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oauth_endpoint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='Критерий')),
            ],
            options={
                'verbose_name': 'Критерий',
                'verbose_name_plural': 'Критерии',
            },
        ),
        migrations.CreateModel(
            name='OwnersMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.FloatField(blank=True, null=True, verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Оценка владельца по критерию',
                'verbose_name_plural': 'Оценки владельца по критериям',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FilePathField(path='static', recursive=True, verbose_name='Путь')),
            ],
            options={
                'verbose_name': 'Ресурс',
                'verbose_name_plural': 'Ресурсы',
            },
        ),
        migrations.CreateModel(
            name='ResourceAccessRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('submitted', models.BooleanField(verbose_name='Подтвержден')),
                ('code', models.CharField(max_length=32)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth_endpoint.Client', verbose_name='Клиент')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.Resource', verbose_name='Ресурс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Инициатор')),
            ],
            options={
                'verbose_name': 'Запрос на получение доступа',
                'verbose_name_plural': 'Запросы на получение доступа',
            },
        ),
        migrations.CreateModel(
            name='ResourceCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(verbose_name='Приоритет')),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.Criteria', verbose_name='Критерий')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criteria', to='resources.Resource', verbose_name='Ресурс')),
            ],
            options={
                'verbose_name': 'Критерий ресурса',
                'verbose_name_plural': 'Критерии ресурса',
            },
        ),
        migrations.CreateModel(
            name='ResourceOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(verbose_name='Приоритет')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='resources.Resource', verbose_name='Ресурс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Владелец ресурса',
                'verbose_name_plural': 'Владельцы ресурса',
            },
        ),
        migrations.AddField(
            model_name='ownersmark',
            name='criteria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.ResourceCriteria', verbose_name='Критерий'),
        ),
        migrations.AddField(
            model_name='ownersmark',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.ResourceOwner', verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='ownersmark',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='resources.ResourceAccessRequest', verbose_name='Запрос'),
        ),
    ]
