# Generated by Django 4.1 on 2022-08-29 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0008_alter_issue_issue_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_views',
            field=models.IntegerField(default=0),
        ),
    ]
