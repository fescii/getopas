# Generated by Django 4.1 on 2022-10-30 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('magazine', '0012_alter_section_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue_likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.RemoveField(
            model_name='issue',
            name='no',
        ),
        migrations.AddField(
            model_name='issue',
            name='link',
            field=models.CharField(default='one', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='owner',
            field=models.CharField(default='femar', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='platform',
            field=models.CharField(default='one', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='release',
            field=models.CharField(default='Ocassionally', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.AddField(
            model_name='issue_likes',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_likes', to='magazine.issue'),
        ),
        migrations.AddField(
            model_name='issue_likes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_users_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
