# Generated by Django 2.2.6 on 2019-12-27 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrbac', '0005_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='按钮权限'),
        ),
    ]
