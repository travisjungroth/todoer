import requests

from allauth.socialaccount import app_settings
from todoist import TodoistAPI

from .provider import TodoistProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class TodoistOAuth2Adapter(OAuth2Adapter):
    provider_id = TodoistProvider.id
    access_token_url = "https://todoist.com/oauth/access_token"
    authorize_url = "https://todoist.com/oauth/authorize"
    scope_delimiter = ','

    def complete_login(self, request, app, token, **kwargs):
        api = TodoistAPI(str(token))
        extra_data = api.user.get()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(TodoistOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(TodoistOAuth2Adapter)
