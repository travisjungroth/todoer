from datetime import datetime

from allauth.socialaccount.models import SocialToken
from django.core.management import BaseCommand
import pytz
from todoist import TodoistAPI

from habits.functions import make_tasks
from habits.models import Task, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                token = SocialToken.objects.get(app__name='Todoist', account__user=user).token
                api = TodoistAPI(token)
                api.sync()
                user_tz = pytz.timezone(api.user.get()['tz_info']['timezone'])
                user.timezone = user_tz
                user.save()
                user_now = datetime.now(user_tz)
                if user_now.hour != 0 or user_now.fold:
                    continue

                try:
                    project_id = api.projects.all(
                        lambda x: x['name'] == 'habits' and not x['is_archived']
                    )[-1]['id']
                except (IndexError, KeyError):
                    continue

                for uncompleted_item in api.projects.get_data(project_id)['items']:
                    api.items.delete(uncompleted_item['id'])

                Task.objects.filter(
                    todoist_id__in=[x['id'] for x in api.items.get_completed(project_id)],
                    habit__user=user,
                ).update(completed=True)

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
