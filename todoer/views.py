from collections import Counter
from datetime import timedelta

from django.utils.timezone import now
from django.views.generic import TemplateView

from todoer.models import Task


class Home(TemplateView):
    template_name = 'home.html'


class WeekScores(TemplateView):
    template_name = 'weekscores.html'

    def get_context_data(self, **kwargs):
        today = now().date()
        a_week_ago = today - timedelta(days=7)
        total = Counter()
        completed = Counter()
        for task in Task.objects.filter(date__gte=a_week_ago, date__lt=today).order_by('order'):
            total[task.template] += 1
            if task.completed:
                completed[task.template] += 1

        d = {}
        for task in Task.objects.filter(date__lt=today).order_by('template__order', 'date'):
            d.setdefault(task.template, []).append(task.completed)

        scores = []
        for template in total:
            streak, goal = f_streak(d[template])
            scores.append(
                {
                    'name': template.name,
                    'completed': completed[template],
                    'total': total[template],
                    'streak': streak,
                    'goal': goal,
                }
            )

        context = super().get_context_data(**kwargs)
        context['scores'] = scores
        context['overall'] = f'{sum(completed.values())}/{sum(total.values())}'
        context['percent'] = f'{round(sum(completed.values()) / sum(total.values()) * 100)}%'
        return context


def f_streak(bools):
    fibonacci = iter((1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987))
    goal = next(fibonacci)
    streak = 0
    for b in bools:
        if streak >= goal:
            streak = 0
            goal = next(fibonacci)
        streak = streak + 1 if b else 0
    return streak, goal
