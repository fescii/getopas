# Generated by Django 4.1 on 2022-08-26 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0002_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='updated',
        ),
    ]