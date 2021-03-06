from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from ordered_model.models import OrderedModel

User = get_user_model()


class Habit(OrderedModel):
    name = models.CharField(max_length=255)
    days = ArrayField(base_field=models.IntegerField())
    morning = models.BooleanField()
    reminder_time = models.CharField(max_length=10, blank=True, default='')
    active = models.BooleanField(default=True)
    streaks = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_with_respect_to = 'user'

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return f'{self.name} on {",".join(map(str, self.days))}'


class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    date = models.DateField(default=now)
    order = models.IntegerField()
    todoist_id = models.BigIntegerField()
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-date', 'order']

    def __str__(self):
        return f'{self.name} on {self.date}'
