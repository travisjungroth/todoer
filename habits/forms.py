from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import modelformset_factory

from habits.models import Habit


HabitFormSet = modelformset_factory(
    Habit,
    fields=['name', 'days', 'morning', 'reminder_time', 'active', 'streaks_and_goals']
)


class HabitFormSetHelper(FormHelper):
    def __init__(self, form=None):
        super().__init__(form)
        self.template = 'bootstrap4/table_inline_formset.html'
        self.add_input(Submit("submit", "Save"))
        self.use_custom_control = False
