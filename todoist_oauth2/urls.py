from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import TodoistProvider


urlpatterns = default_urlpatterns(TodoistProvider)
