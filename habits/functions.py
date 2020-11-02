from django.utils.timezone import now

from habits.models import Task, Habit


def generate_streaks_and_goals(habits, today):
    d = {}
    for task in Task.objects.select_related('habit').filter(date__lt=today, habit__in=habits).order_by(
            'habit__order', 'date'):
        d.setdefault(task.habit, []).append(task.completed)
    return {habit: f_streak(bools) for habit, bools in d.items()}


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


def make_tasks(morning, api, user_now, user):
    ids = []
    habits = Habit.objects.filter(active=True, morning=morning, days__contains=[user_now.weekday()], user=user)
    streaks_and_goals = generate_streaks_and_goals(habits, user_now.date())
    for habit in habits:
        if habit.streaks_and_goals:
            streak, goal = streaks_and_goals[habit]
            text = f'{habit.name} [{streak}/{goal}] #habits today'
        else:
            text = f'{habit.name} #habits today'
        item = api.quick.add(text, reminder=habit.reminder_time)
        Task.objects.create(
            name=habit.name,
            date=user_now.date(),
            order=habit.order,
            todoist_id=item['id'],
            habit=habit,
        )
        ids.append(item['id'])
    return ids
