import factory
from django.contrib.contenttypes.models import ContentType

from complaint.choices import ComplaintStatusChoices
from complaint.models import Complaint


class ComplaintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Complaint

    # assumes you have an Account/User factory at account.factories.UserFactory
    creator = factory.SubFactory('account.factories.UserFactory')
    details = factory.Faker('paragraph')
    status = ComplaintStatusChoices.REGISTERED.value

    # by default no generic relation
    related_content_type = None
    related_object_id = None

    @factory.post_generation
    def with_related_object(self, create, extracted, **kwargs):
        """
        To attach a related object, pass it in as:
            ComplaintFactory(with_related_object=some_model_instance)
        """
        if not create or not extracted:
            return
        self.related_content_type = ContentType.objects.get_for_model(extracted)
        self.related_object_id = extracted.pk
        self.save()
    