# Generated by Django 4.1 on 2022-08-29 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='blog_views',
            field=models.IntegerField(default=0),
        ),
    ]