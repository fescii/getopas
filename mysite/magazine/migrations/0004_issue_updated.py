# Generated by Django 4.1 on 2022-08-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0003_remove_issue_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
