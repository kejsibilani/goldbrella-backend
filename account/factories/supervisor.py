import factory
from django.contrib.auth.models import Group

from account.choices import UserRoleChoices
from account.factories import UserFactory
from account.models import User


class SupervisorFactory(UserFactory):
    class Meta:
        model = User

    # set the role field on your custom User model
    role = UserRoleChoices.SUPERVISOR.value  # or simply 'supervisor'

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """
        After the user is created, make sure they belong to the Supervisor group.
        """
        if not create:
            # Simple build, no DB, nothing to do
            return
        group, _ = Group.objects.get_or_create(name="Supervisor")
        self.groups.add(group)
