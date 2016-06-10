# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 18:30
from __future__ import unicode_literals

import AuthorizationServer.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('secret', models.CharField(default=AuthorizationServer.utils.generate_client_secret, max_length=32)),
                ('redirect_uri', models.CharField(blank=True, max_length=127, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
