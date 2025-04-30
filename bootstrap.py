import os, django
import traceback
from random import choice


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldBrella.settings')
django.setup()


from django.db import connection, DatabaseError
from django.contrib.auth.models import Permission
from django.core.management import call_command

from account.factories import UserFactory
from account.factories import GroupFactory
from beach.factories import BeachLocationFactory
from beach.factories import BeachFactory
from beach.factories import BeachImageFactory
from booking.factories import BookingFactory
from inventory.factories import InventoryItemFactory
from payment.factories import BookingPaymentFactory
from sunbed.factories import SunbedFactory


def clear_database():
    with connection.cursor() as cursor:
        try:
            cursor.execute('DROP SCHEMA IF EXISTS PUBLIC CASCADE;')
            cursor.execute('CREATE SCHEMA PUBLIC;')
            cursor.execute('ALTER SCHEMA PUBLIC OWNER TO postgres')
        except DatabaseError: traceback.print_exc()


def crud(model: str, c: bool = True, r: bool = True, u: bool = True, d: bool = True):
    perms = []
    if c: perms.append(f'add_{model}')
    if r: perms.append(f'view_{model}')
    if u: perms.append(f'change_{model}')
    if d: perms.append(f'delete_{model}')
    return perms

# Set the permissions for guest and staff
guest_permission_set = {
    *crud('booking'),
    *crud('bookingpayment', c=False, u=False, d=False),
}

staff_permission_set = {
    *crud('booking'),
    *crud('user', d=False),
    *crud('bookingpayment', c=False, d=False),
}

# Clear the database
clear_database()
print('..................... DATABASE CLEARED .....................')
# call_command('flush', '--no-input')
call_command('migrate', '-v', '0', '--no-input')
print('..................... DATABASE MIGRATED .....................')
print(f'..................... DATA SEEDING STARTED .....................')
# Create Staff and Guest Groups
guest_permissions = Permission.objects.filter(codename__in=guest_permission_set)
guest_group = GroupFactory.create(name='Staff', permissions=guest_permissions)
print('..................... STAFF GROUP CREATED .....................')
staff_permissions = Permission.objects.filter(codename__in=staff_permission_set)
staff_group = GroupFactory.create(name='Guest', permissions=staff_permissions)
print('..................... GUEST GROUP CREATED .....................')
# Create Super User
UserFactory.create(email='admin@xyz.com', is_superuser=True)
print('..................... SUPERUSER CREATED .....................')
# Create Guest and Staff
UserFactory.create(email='staff@xyz.com', is_staff=True, is_superuser=False, groups=[staff_group])
staff = UserFactory.create_batch(9, is_staff=True, is_superuser=False, groups=[staff_group])
print('..................... STAFF CREATED .....................')
UserFactory.create(email='guest@xyz.com', is_staff=False, is_superuser=False, groups=[guest_group])
guests = UserFactory.create_batch(49, is_staff=False, is_superuser=False, groups=[guest_group])
print('..................... GUESTS CREATED .....................')
# Create Location, Beach and Sunbeds
locations = BeachLocationFactory.create_batch(15)
print('..................... LOCATIONS ADDED .....................')
for location in locations:
    beaches = BeachFactory.create_batch(2, location=location)
    print(f'..................... BEACHES FOR {location.city.upper()} ADDED .....................')
    for beach in beaches:
        BeachImageFactory.create_batch(10, beach=beach)
        print(f'..................... IMAGES FOR {beach.title.upper()} ADDED .....................')
        SunbedFactory.create_batch(50, beach=beach)
        print(f'..................... SUNBEDS FOR {beach.title.upper()} ADDED .....................')
        InventoryItemFactory.create_batch(50, beach=beach)
        print(f'..................... INVENTORY ITEMS FOR {beach.title.upper()} ADDED .....................')
        BookingFactory.create_batch(5, beach=beach, user=choice(guests), booked_by=choice(staff))
        print(f'..................... STAFF BOOKINGS FOR {beach.title.upper()} ADDED .....................')
        for _ in range(5):
            guest = choice(guests)
            booking = BookingFactory.create(beach=beach, user=guest, booked_by=guest)
            BookingPaymentFactory.create(booking=booking)
        print(f'..................... SELF BOOKINGS WITH PAYMENTS FOR {beach.title.upper()} ADDED .....................')
print(f'..................... DATA SEEDING COMPLETED .....................')
