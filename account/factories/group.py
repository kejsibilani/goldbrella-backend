import factory
from django.contrib.auth.models import Group, Permission


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    # auto-incrementing name: “group_0”, “group_1”, …
    name = factory.Sequence(lambda n: f"Group {n}")

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        """
        Usage:
            # no permissions
            GroupFactory()

            # pass a list of Permission instances (or pks)
            perms = Permission.objects.filter(codename__in=["add_user", "change_user"])
            GroupFactory(permissions=perms)
        """
        if not create:
            return

        if extracted:
            for perm in extracted:
                if isinstance(perm, Permission):
                    self.permissions.add(perm)
                else:
                    self.permissions.add(Permission.objects.get(pk=perm))
