import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
django.setup()

from account.models import User
from beach.models import Beach
from beach.models import BeachImage
from location.models import Location
from sunbed.models import Sunbed
from zone.models import Zone
import requests
from django.core.files.base import ContentFile

# 1. Delete all users except 'kejsi bilani'
users = User.objects.exclude(first_name__iexact='kejsi').exclude(last_name__iexact='bilani')
print(f"Deleting {users.count()} users...")
users.delete()

# 2. Delete all beaches
beaches = Beach.objects.all()
print(f"Deleting {beaches.count()} beaches...")
beaches.delete()

# 3. Delete all locations except Vlore and Dhermi
locations = Location.objects.exclude(city__in=['Vlore', 'Dhermi'])
print(f"Deleting {locations.count()} locations...")
locations.delete()

# 4. Create/ensure only Vlore and Dhermi exist
vlore_location, _ = Location.objects.get_or_create(city='Vlore', country='AL')
dhermi_location, _ = Location.objects.get_or_create(city='Dhermi', country='AL')

# 5. Add beaches to each location, with sunbed counts
beach_data = [
    # Vlore beaches
    {"title": "Plazhi i Ri", "latitude": 40.4462, "longitude": 19.4897, "location": vlore_location, "sunbeds": 30},
    {"title": "Uji i Ftohte", "latitude": 40.4297, "longitude": 19.4890, "location": vlore_location, "sunbeds": 20},
    {"title": "Radhime Beach", "latitude": 40.3825, "longitude": 19.4711, "location": vlore_location, "sunbeds": 15},
    # Dhermi beaches
    {"title": "Dhërmi Beach", "latitude": 40.1531, "longitude": 19.6347, "location": dhermi_location, "sunbeds": 40},
    {"title": "Drymades Beach", "latitude": 40.1481, "longitude": 19.6297, "location": dhermi_location, "sunbeds": 25},
]

for i, b in enumerate(beach_data):
    beach = Beach.objects.create(
        title=b["title"],
        latitude=b["latitude"],
        longitude=b["longitude"],
        location=b["location"]
    )
    # Add 3 photos per beach
    for j in range(3):
        img_url = f"https://loremflickr.com/800/600/beach?random={i*10+j+1}"
        resp = requests.get(img_url)
        if resp.status_code == 200:
            img_name = f"{beach.title.replace(' ', '_').lower()}_{j+1}.jpg"
            BeachImage.objects.create(
                beach=beach,
                image=ContentFile(resp.content, name=img_name)
            )
            print(f"Added photo {j+1} for {beach.title}")
        else:
            print(f"Failed to fetch image {j+1} for {beach.title}")
    # Add sunbeds (all to first zone)
    zone = Zone.objects.filter(beach=beach).first()
    if zone:
        for k in range(b["sunbeds"]):
            Sunbed.objects.create(
                zone=zone,
                area="A",
                identity=f"{beach.title[:3].upper()}-{k+1:03d}",
                price=10.0
            )
        print(f"Added {b['sunbeds']} sunbeds to {beach.title}")
    else:
        print(f"No zone found for {beach.title}, sunbeds not added.")
print(f"Added {len(beach_data)} beaches with sunbeds and photos, in 2 locations.") 