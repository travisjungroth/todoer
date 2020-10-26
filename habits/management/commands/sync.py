from datetime import datetime

from django.core.management import BaseCommand
import pytz
from todoist import TodoistAPI

from habits.functions import make_tasks
from habits.models import Task, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.exclude(profile__api_token=''):
            try:
                api = TodoistAPI(user.profile.api_token)
                user_tz = pytz.timezone(api.user.get()['tz_info']['timezone'])
                user_now = datetime.now(user_tz)
                if user_now.hour != 0 or user_now.fold:
                    continue

                project_id = api.projects.all(
                    lambda x: x['name'] == user.profile.project_name and not x['is_archived']
                )[-1]['id']

                for uncompleted_item in api.projects.get_data(project_id)['items']:
                    api.items.delete(uncompleted_item['id'])

                for completed_item in api.items.get_completed(project_id):
                    try:
                        task = Task.objects.get(todoist_id=completed_item['id'], habit__user=user)
                        task.completed = True
                        task.save()
                    except Task.DoesNotExist:
                        pass
                    api.items.delete(completed_item['id'])

                api.commit(raise_on_error=True)
                api.sync()
                today_str = str(user_now.date())
                existing_today_tasks = [task['id'] for task in api['items'] if
                                        task['due'] is not None and task['due']['date'] == today_str]
                ids = make_tasks(morning=True, api=api, user_now=user_now, user=user)
                ids.extend(existing_today_tasks)
                ids.extend(make_tasks(morning=False, api=api, user_now=user_now, user=user))
                ids_to_orders = {id_: i for i, id_ in enumerate(ids)}
                api.items.update_day_orders(ids_to_orders)
                api.commit(raise_on_error=True)
            except Exception as e:
                print(e)
