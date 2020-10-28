from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class TodoistAccount(ProviderAccount):
    pass


class TodoistProvider(OAuth2Provider):
    id = "todoist"
    name = "Todoist"
    account_class = TodoistAccount

    def extract_uid(self, data):
        print(repr(data))
        return str(data["email"])

    def extract_common_fields(self, data):
        return {"name": data.get("full_name"), "email": data.get("email")}

    def get_default_scope(self):
        return ['data:read']


provider_classes = [TodoistProvider]
