from django.utils.timezone import now

from todoer.models import Task, TaskTemplate


def generate_streaks_and_goals(templates):
    today = now().date()
    d = {}
    for task in Task.objects.select_related('template').filter(date__lt=today, template__in=templates).order_by(
            'template__order', 'date'):
        d.setdefault(task.template, []).append(task.completed)
    return {template: f_streak(bools) for template, bools in d.items()}


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


def make_tasks(morning, api):
    ids = []
    templates = TaskTemplate.objects.filter(active=True, morning=morning,
                                            schedule__days__contains=[now().weekday()])
    streaks_and_goals = generate_streaks_and_goals(templates)
    for template in templates:
        if template.streaks_and_goals:
            streak, goal = streaks_and_goals[template]
            text = f'{template.name} [{streak}/{goal}] #habits today'
        else:
            text = f'{template.name} #habits today'
        item = api.quick.add(text, reminder=template.reminder_time)
        Task.objects.create(name=template.name, order=template.order, todoist_id=item['id'], template=template)
        ids.append(item['id'])
    return ids
