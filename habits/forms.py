from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from habits.models import Habit


class HabitForm(forms.ModelForm):
    days = forms.TypedMultipleChoiceField(
        choices=enumerate('MTWTFSS'),
        coerce=int,
        empty_value=None,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Habit
        fields = ['name', 'days', 'morning', 'reminder_time', 'active', 'show_streaks']


HabitFormSet = forms.modelformset_factory(
    Habit,
    form=HabitForm,
    extra=1,
)


class HabitFormSetHelper(FormHelper):
    def __init__(self, form=None):
        super().__init__(form)
        self.template = 'table_inline_formset.html'
        self.add_input(Submit("submit", "Save"))
