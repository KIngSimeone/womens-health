# Generated by Django 3.2.5 on 2021-07-21 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccessTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(null=True)),
                ('access_token', models.TextField(verbose_name='access_token')),
                ('expires_at', models.DateTimeField(verbose_name='expires_at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
            ],
            options={
                'verbose_name': 'User Access Token',
                'verbose_name_plural': 'User Access Tokens',
            },
        ),
    ]
