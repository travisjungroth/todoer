from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from ordered_model.models import OrderedModel


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    days = ArrayField(base_field=models.IntegerField())

    def __str__(self):
        return self.name


class TaskTemplate(OrderedModel):
    name = models.CharField(max_length=255)
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    morning = models.BooleanField()
    reminder_time = models.CharField(max_length=10, help_text='like 9pm', blank=True, default='')

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return f'{self.name} on {self.schedule.name.lower()}'


class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    date = models.DateField(default=now)
    order = models.IntegerField()
    todoist_id = models.BigIntegerField()
    template = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date', 'order']

    def __str__(self):
        return f'{self.name} on {self.date}'
