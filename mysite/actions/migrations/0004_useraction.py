# Generated by Django 4.1 on 2022-11-11 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actions', '0003_action_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('read', 'Read'), ('unread', 'Unread')], default='unread', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='actions.action')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
