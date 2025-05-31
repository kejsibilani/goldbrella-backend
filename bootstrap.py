import os
import traceback
from random import choice
from random import choices
from random import randint

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
django.setup()


from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.db import DatabaseError
from django.db import connection

from account.factories import GroupFactory
from account.factories import UserFactory
from account.settings import GUEST_USER_PERMISSION_SET
from account.settings import STAFF_USER_PERMISSION_SET
from beach.factories import BeachFactory
from beach.factories import BeachImageFactory
from booking.factories import BookingFactory
from inventory.factories import InventoryItemFactory
from location.factories import LocationFactory
from sunbed.factories import SunbedFactory
from zone.factories import ZoneFactory


def clear_database():
    try:
        DBUSER = settings.DATABASES.get('default', {}).get('USER', 'postgres')
    except (KeyError, AttributeError, IndexError):
        DBUSER = 'postgres'

    with connection.cursor() as cursor:
        try:
            cursor.execute('DROP SCHEMA IF EXISTS PUBLIC CASCADE;')
            cursor.execute('CREATE SCHEMA PUBLIC;')
            cursor.execute(f'ALTER SCHEMA PUBLIC OWNER TO {DBUSER}')
        except DatabaseError: traceback.print_exc()


sunbeds = []
# Clear the database
clear_database()
print('..................... DATABASE CLEARED .....................')
# call_command('flush', '--no-input')
call_command('migrate', '-v', '0', '--no-input')
print('..................... DATABASE MIGRATED .....................')
print(f'..................... DATA SEEDING STARTED .....................')
# Create Staff and Guest Groups
guest_permissions = Permission.objects.filter(codename__in=GUEST_USER_PERMISSION_SET)
guest_group = GroupFactory.create(name='Staff', permissions=guest_permissions)
print('..................... STAFF GROUP CREATED .....................')
staff_permissions = Permission.objects.filter(codename__in=STAFF_USER_PERMISSION_SET)
staff_group = GroupFactory.create(name='Guest', permissions=staff_permissions)
print('..................... GUEST GROUP CREATED .....................')
# Create Super User
UserFactory.create(email='admin@xyz.com', role='admin', is_superuser=True)
print('..................... SUPERUSER CREATED .....................')
# Create Guest, Staff and Supervisor
UserFactory.create(email='supervisor@xyz.com', role='supervisor', is_superuser=False, groups=[staff_group])
supervisor = UserFactory.create_batch(4, role='supervisor', is_superuser=False, groups=[staff_group])
print('..................... SUPERVISOR CREATED .....................')
UserFactory.create(email='staff@xyz.com', role='staff', is_superuser=False, groups=[staff_group])
staff = UserFactory.create_batch(9, role='staff', is_superuser=False, groups=[staff_group])
print('..................... STAFF CREATED .....................')
UserFactory.create(email='guest@xyz.com', role='guest', is_superuser=False, groups=[guest_group])
guests = UserFactory.create_batch(49, role='guest', is_superuser=False, groups=[guest_group])
print('..................... GUESTS CREATED .....................')
# Create Location, Beach and Sunbeds
locations = LocationFactory.create_batch(15)
print('..................... LOCATIONS ADDED .....................')
for location in locations:
    beaches = BeachFactory.create_batch(2, location=location)
    print(f'..................... BEACHES FOR {location.city.upper()} ADDED .....................')
    for beach in beaches:
        BeachImageFactory.create_batch(10, beach=beach)
        print(f'..................... IMAGES FOR {beach.title.upper()} ADDED .....................')
        InventoryItemFactory.create_batch(50, beach=beach)
        print(f'..................... INVENTORY ITEMS FOR {beach.title.upper()} ADDED .....................')
        zones = ZoneFactory.create_batch(2, beach=beach)
        print(f'..................... ZONES FOR {beach.title.upper()} ADDED .....................')
        for zone in zones:
            sunbeds = SunbedFactory.create_batch(50, zone=zone)
            print(f'..................... SUNBEDS {zone.location.upper()} FOR {beach.title.upper()} ADDED .....................')
        BookingFactory.create_batch(5, beach=beach, user=choice(guests), booked_by=choice(staff), sunbeds=choices(sunbeds, k=randint(1, 3)))
        print(f'..................... STAFF BOOKINGS FOR {beach.title.upper()} ADDED .....................')
        for _ in range(5):
            guest = choice(guests)
            booking = BookingFactory.create(beach=beach, user=guest, booked_by=guest)
        print(f'..................... SELF BOOKINGS WITH PAYMENTS FOR {beach.title.upper()} ADDED .....................')
print(f'..................... DATA SEEDING COMPLETED .....................')
