from django.forms import modelformset_factory

from habits.models import Habit

fields = ['name', 'days', 'morning', 'reminder_time', 'active', 'streaks_and_goals']
HabitFormSet = modelformset_factory(Habit, fields=fields, can_delete=True)
