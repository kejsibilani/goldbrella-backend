import random
from django.core.management.base import BaseCommand
from inventory.models import InventoryItem
from beach.models import Beach

# Menu item templates by category
COCKTAILS = [
    ("Mojito", "A refreshing Cuban cocktail", 12.0),
    ("Pina Colada", "Coconut cream, pineapple juice, and white rum", 13.0),
    ("Caipirinha", "Brazilian classic with lime and cachaça", 11.0),
    ("Aperol Spritz", "Aperol, prosecco, and soda", 10.0),
    ("Margarita", "Tequila, lime, and triple sec", 12.5),
    ("Mai Tai", "Rum, lime, and almond syrup", 13.5),
]
FOOD = [
    ("Beach Burger", "Juicy grilled burger with beach vibes", 15.0),
    ("Fish Tacos", "Crispy fish with fresh salsa", 13.5),
    ("Cheese Bread", "Brazilian pão de queijo", 6.0),
    ("Caesar Salad", "Classic Caesar with croutons", 11.0),
    ("Nachos Supreme", "Loaded nachos with cheese and salsa", 9.5),
    ("Grilled Shrimp Skewers", "Fresh shrimp, grilled to perfection", 14.0),
]
NON_ALCOHOLIC = [
    ("Iced Coffee", "Chilled coffee for hot days", 5.5),
    ("Fresh Coconut", "Served in the shell", 4.5),
    ("Fruit Smoothie", "Mixed tropical fruits", 7.5),
    ("Sparkling Lemonade", "Homemade lemonade with bubbles", 4.0),
    ("Mineral Water", "Still or sparkling", 2.5),
]
BEER = [
    ("Beach Lager", "Crisp and cold", 6.0),
    ("Premium IPA", "Hoppy and refreshing", 7.0),
]
WINE = [
    ("Chardonnay", "Chilled white wine", 8.0),
    ("Rosé", "Perfect for the beach", 8.5),
]

CATEGORY_MAP = [
    (COCKTAILS, "Cocktails"),
    (FOOD, "Food"),
    (NON_ALCOHOLIC, "Non-Alcoholic"),
    (BEER, "Beer"),
    (WINE, "Wine"),
]

class Command(BaseCommand):
    help = "Populate a unique menu for each beach."

    def handle(self, *args, **options):
        beaches = Beach.objects.all()
        if not beaches.exists():
            self.stdout.write(self.style.ERROR("No beaches found. Please create beaches first."))
            return

        created_count = 0
        for idx, beach in enumerate(beaches):
            random.seed(beach.id)  # Ensure reproducibility per beach
            menu_items = []
            # Each beach gets a random selection from each category
            for items, category in CATEGORY_MAP:
                n = random.randint(2, min(4, len(items)))
                chosen = random.sample(items, n)
                for name, desc, price in chosen:
                    menu_items.append({
                        "name": f"{beach.title} {name}" if random.random() < 0.3 else name,  # Some items themed
                        "description": desc,
                        "price": price + random.uniform(-1, 2),
                        "category": category,
                        "quantity": random.randint(50, 200),
                        "reusable_item": False,
                    })
            for item in menu_items:
                obj, created = InventoryItem.objects.get_or_create(
                    name=item["name"],
                    beach=beach,
                    defaults={
                        "category": item["category"],
                        "price": round(item["price"], 2),
                        "quantity": item["quantity"],
                        "reusable_item": item["reusable_item"],
                    }
                )
                if created:
                    created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created_count} unique menu items for all beaches.")) 