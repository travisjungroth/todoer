from collections import Counter
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, FormView, DeleteView

from habits.forms import HabitFormSet, HabitFormSetHelper, TaskFormSetHelper, TaskFormSet
from habits.functions import generate_streaks_and_goals
from habits.models import Task, Habit


class Home(TemplateView):
    template_name = 'home.html'


class HabitView(LoginRequiredMixin, FormView):
    template_name = 'habits/habits.html'
    form_class = HabitFormSet

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['queryset'] = Habit.objects.filter(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        for inner_form in form.forms:
            inner_form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = HabitFormSetHelper()
        context['formset'] = context.pop('form')
        context['directions'] = HabitMove.allowed_directions
        return context


class HabitMove(LoginRequiredMixin, View):
    allowed_directions = ('top', 'up', 'down', 'bottom')

    def get(self, request, pk, direction):
        if direction not in self.allowed_directions:
            raise Http404()
        habit = get_object_or_404(Habit, pk=pk, user=self.request.user)
        getattr(habit, direction)()
        return HttpResponseRedirect(reverse('habits'))


class HabitDelete(DeleteView):
    model = Habit
    success_url = reverse_lazy('habits')


class TaskView(LoginRequiredMixin, FormView):
    template_name = 'habits/tasks.html'
    form_class = TaskFormSet
    success_url = reverse_lazy('tasks')

    def get_form_kwargs(self):
        return super().get_form_kwargs() | {'queryset': Task.objects.filter(habit__user=self.request.user)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['helper'] = TaskFormSetHelper()
        context['formset'] = context.pop('form')
        return context


class WeekScores(TemplateView):
    template_name = 'habits/weekscores.html'

    def get_context_data(self, **kwargs):
        today = now().date()
        a_week_ago = today - timedelta(days=7)
        total = Counter()
        completed = Counter()
        for task in Task.objects.select_related('habit').filter(date__gte=a_week_ago, date__lt=today).order_by('order'):
            total[task.habit] += 1
            if task.completed:
                completed[task.habit] += 1

        streaks_and_goals = generate_streaks_and_goals(total)
        scores = []
        for habit in total:
            streak, goal = streaks_and_goals[habit]
            scores.append(
                {
                    'name': habit.name,
                    'completed': completed[habit],
                    'total': total[habit],
                    'streak': streak,
                    'goal': goal,
                }
            )

        context = super().get_context_data(**kwargs)
        context['scores'] = scores
        context['overall'] = f'{sum(completed.values())}/{sum(total.values())}'
        try:
            context['percent'] = f'{round(sum(completed.values()) / sum(total.values()) * 100)}%'
        except ZeroDivisionError:
            context['percent'] = '0%'
        return context
