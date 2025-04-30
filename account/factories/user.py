from random import choices
from string import digits

import factory
from django.contrib.auth.models import Group

from account.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    # Because your USERNAME_FIELD is email:
    email = factory.Faker('safe_email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    address = factory.Faker('address')
    preferred_language = factory.Faker('language_name')
    assigned_area = factory.Faker('city')
    department = factory.Faker('word')
    is_superuser = factory.Faker('boolean')
    is_staff = factory.Faker('boolean')
    phone_number = factory.LazyFunction(
        lambda: "".join(choices(digits, k=13))
    )
    office_contact = factory.LazyFunction(
        lambda: "".join(choices(digits, k=13))
    )

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """
        Usage:
            # no groups
            UserFactory()

            # pass existing Group instances (or PKs)
            some_groups = Group.objects.filter(name__in=["Editors", "Moderators"])
            UserFactory(groups=some_groups)

            # or automatically create 2 random groups via GroupFactory
            UserFactory(groups=[GroupFactory(), GroupFactory()])
        """
        if not create:
            return

        if extracted:
            for group in extracted:
                if isinstance(group, Group):
                    self.groups.add(group)
                else:
                    self.groups.add(Group.objects.get(pk=group))
