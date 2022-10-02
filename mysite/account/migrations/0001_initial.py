# Generated by Django 4.1 on 2022-10-02 12:01

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField()),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('occupation', models.TextField()),
                ('website', models.CharField(blank=True, max_length=250)),
                ('twitter', models.CharField(blank=True, max_length=250)),
                ('linkedin', models.CharField(blank=True, max_length=250)),
                ('location', models.CharField(blank=True, max_length=250)),
                ('photo', models.ImageField(blank=True, upload_to='users/%Y/%m/%d')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]