import random

import factory
import requests
from django.core.files.base import ContentFile

from beach.factories.beach import BeachFactory
from beach.models import BeachImage

BEACH_SYNONYMS = [
    "beach",
    "coast",
    "seashore",
    "shore",
    "seaside",
    "coastline",
    "strand",
    "sandy+beach",
]

class BeachImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeachImage

    beach = factory.SubFactory(BeachFactory)

    @factory.lazy_attribute
    def image(self):
        # randomly pick one of the synonyms:
        tag = random.choice(BEACH_SYNONYMS)
        # LoremFlickr: width=800, height=600, by tag, + cache-busting random
        url = f"https://loremflickr.com/800/600/{tag}?random={random.randint(1,1_000_000)}"
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        # name file after the tag so you can tell them apart
        filename = f"{tag.replace('+', '_')}.jpg"
        return ContentFile(resp.content, name=filename)
