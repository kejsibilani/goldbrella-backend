from django.test import TestCase
from sunbed.models import Sunbed
from zone.models import Zone
from django.contrib.auth import get_user_model

# Create your tests here.

class SunbedRowColumnTestCase(TestCase):
    def setUp(self):
        # Create a dummy zone (requires a user and a beach, but we keep it minimal)
        User = get_user_model()
        user = User.objects.create(username='testuser')
        from beach.models import Beach
        from location.models import Location
        location = Location.objects.create(city='Test City', country='AL')
        beach = Beach.objects.create(title='Test Beach', latitude=40.0, longitude=19.0, location=location)
        self.zone = Zone.objects.create(location='A', beach=beach, supervisor=user)

    def test_create_sunbed_with_row_and_column(self):
        sunbed = Sunbed.objects.create(
            zone=self.zone,
            area='A',
            identity='A-01',
            price=10.0,
            row=2,
            column=5
        )
        self.assertEqual(sunbed.row, 2)
        self.assertEqual(sunbed.column, 5)
        # Fetch from DB and check
        sunbed_db = Sunbed.objects.get(pk=sunbed.pk)
        self.assertEqual(sunbed_db.row, 2)
        self.assertEqual(sunbed_db.column, 5)
