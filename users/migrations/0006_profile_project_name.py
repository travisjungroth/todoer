# Generated by Django 3.1.2 on 2020-10-24 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201024_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='project_name',
            field=models.CharField(default='habits', max_length=255),
        ),
    ]