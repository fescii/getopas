# Generated by Django 4.1 on 2022-09-01 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_alter_physicalinfo_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default='Samsung', max_length=250),
            preserve_default=False,
        ),
    ]