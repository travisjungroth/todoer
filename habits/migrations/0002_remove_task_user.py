# Generated by Django 3.1.2 on 2020-10-26 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_squashed_0005_auto_20201026_0151_squashed_0002_auto_20201026_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]
