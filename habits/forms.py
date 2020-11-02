from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from habits.models import Habit

HabitFormSet = forms.modelformset_factory(
    Habit,
    fields=['name', 'days', 'morning', 'reminder_time', 'active', 'show_streaks'],
    can_delete=True,
    extra=1,
)


class HabitFormSetHelper(FormHelper):
    def __init__(self, form=None):
        super().__init__(form)
        self.template = 'bootstrap4/table_inline_formset.html'
        self.add_input(Submit("submit", "Save"))
