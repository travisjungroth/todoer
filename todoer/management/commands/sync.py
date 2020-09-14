from datetime import date
import json
import uuid

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.timezone import now
import requests
from todoist import TodoistAPI

from todoer.models import Task, TaskTemplate

HABITS = 2223119914


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = TodoistAPI(settings.TODOIST_TOKEN)
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

        def make_tasks(morning):
            ids = []
            for template in TaskTemplate.objects.filter(morning=morning, schedule__days__contains=[now().weekday()]):
                item = api.quick.add(f'{template.name} #habits today', reminder=template.reminder_time)
                Task.objects.create(name=template.name, order=template.order, todoist_id=item['id'])
                ids.append(item['id'])
            return ids

        today = str(date.today())
        existing_today_tasks = [task['id'] for task in api['items'] if
                                task['due'] is not None and task['due']['date'] == today]
        ids = make_tasks(morning=True)
        ids.extend(existing_today_tasks)
        ids.extend(make_tasks(morning=False))
        ids_to_orders = {id_: i for i, id_ in enumerate(ids)}
        api.items.update_day_orders(ids_to_orders)
        api.commit(raise_on_error=True)
