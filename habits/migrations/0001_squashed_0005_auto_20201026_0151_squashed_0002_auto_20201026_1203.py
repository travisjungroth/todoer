# Generated by Django 3.1.2 on 2020-10-26 12:05

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('name', models.CharField(max_length=255)),
                ('morning', models.BooleanField()),
                ('reminder_time', models.CharField(blank=True, default='', help_text='like 9pm', max_length=10)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
                ('streaks_and_goals', models.BooleanField(default=True)),
                ('days', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('completed', models.BooleanField(default=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('order', models.IntegerField()),
                ('todoist_id', models.BigIntegerField()),
                (
                'habit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'ordering': ['-date', 'order'],
            },
        ),
    ]
