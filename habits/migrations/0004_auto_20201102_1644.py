# Generated by Django 3.1.2 on 2020-11-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_auto_20201026_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='reminder_time',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]