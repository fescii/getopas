# Generated by Django 4.1 on 2022-08-29 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0006_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='magazine.issue'),
        ),
    ]
