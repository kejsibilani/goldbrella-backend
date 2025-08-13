import os
import qrcode
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
django.setup()

from beach.models import Beach
from sunbed.models import Sunbed

FRONTEND_URL = 'https://your-frontend.com/menu'
OUTPUT_DIR = 'qr_codes'

os.makedirs(OUTPUT_DIR, exist_ok=True)

beaches = Beach.objects.all()[:2]
for beach in beaches:
    sunbeds = Sunbed.objects.filter(zone__beach=beach)[:3]
    for sunbed in sunbeds:
        url = f"{FRONTEND_URL}?beach_id={beach.id}&sunbed={sunbed.id}"
        img = qrcode.make(url)
        filename = f"{OUTPUT_DIR}/beach_{beach.id}_sunbed_{sunbed.id}.png"
        img.save(filename)
        print(f"Generated QR code: {filename} -> {url}") 