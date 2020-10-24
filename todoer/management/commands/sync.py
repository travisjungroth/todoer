from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from todoist import TodoistAPI

from todoer.functions import make_tasks
from todoer.models import Task

HABITS = 2223119914


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = get_user_model().get()
        api = TodoistAPI(user.profile.api_token)
        api.sync()

        for uncompleted_item in api.projects.get_data(HABITS)['items']:
            api.items.delete(uncompleted_item['id'])

        for completed_item in api.items.get_completed(HABITS):
            try:
                task = Task.objects.get(todoist_id=completed_item['id'])
                task.completed = True
                task.save()
            except Task.DoesNotExist:
                pass
            api.items.delete(completed_item['id'])

        api.commit(raise_on_error=True)
        api.sync()

        today = str(date.today())
        existing_today_tasks = [task['id'] for task in api['items'] if
                                task['due'] is not None and task['due']['date'] == today]
        ids = make_tasks(morning=True, api=api)
        ids.extend(existing_today_tasks)
        ids.extend(make_tasks(morning=False, api=api))
        ids_to_orders = {id_: i for i, id_ in enumerate(ids)}
        api.items.update_day_orders(ids_to_orders)
        api.commit(raise_on_error=True)
