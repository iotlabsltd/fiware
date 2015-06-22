from oauth2_provider.models import get_application_model
from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory


Application = get_application_model()
User = get_user_model()


class AccountFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('email',)

    password = factory.PostGenerationMethodCall("set_password", "123456")
    email = "user1@example.com"
    is_active = True
    is_staff = False
    is_superuser = False
    username = factory.LazyAttribute(lambda obj: obj.email.split("@")[0])


class OAuth2ApplicationFactory(DjangoModelFactory):

    class Meta:
        model = Application
        django_get_or_create = ('name',)

    client_id = "1rWR08jZRYyQcQVL2MY57hs7aE1S7gHwSrD13Jup"
    client_secret = "RKOfXgABtMUKdc7FsvdnL7yBhnZMep2HvGoCIsVIxBOktX58PlShWLmZ1OdRRdbIWxtoDWqbXBtJjQVOYYynsU2SPXiGG5bUAoaFbxTF5jEjCa9ocq30OU3RrxxLmfuV"
    user = factory.SubFactory(AccountFactory)
    redirect_uris = "https://example.com/redirect"
    client_type = Application.CLIENT_PUBLIC
    authorization_grant_type = Application.GRANT_PASSWORD
    name = "test_client"


class TestModelFactory(DjangoModelFactory):

    class Meta:
        model = "tests.TestModel"

    c = "Foo"
    i = 11
