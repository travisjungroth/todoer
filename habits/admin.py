from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from habits import models


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Habit)
class HabitAdmin(OrderedModelAdmin):
    list_display = ('edit', 'name', 'schedule', 'morning', 'reminder_time', 'move_up_down_links', 'active')
    list_editable = ('name', 'schedule', 'morning', 'reminder_time', 'active')

    def edit(self, _):
        return 'edit'


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'completed', 'date')
    list_editable = ('completed',)
