from django.core.management.base import BaseCommand
from store.models import Product
DATA = [("Ceramic Pour-Over Set","Hand-glazed dripper and server for slow mornings.",1899,"https://picsum.photos/seed/pour/600/450"),
("Linen Tote Bag","Heavy linen, reinforced handles, fits a laptop.",799,"https://picsum.photos/seed/tote/600/450"),
("Walnut Desk Tray","Solid walnut organiser for pens and cables.",1299,"https://picsum.photos/seed/tray/600/450"),
("Notebook Trio","Three dot-grid notebooks, stitched binding.",449,"https://picsum.photos/seed/notes/600/450"),
("Brass Desk Lamp","Adjustable arm, warm LED bulb included.",2799,"https://picsum.photos/seed/lamp/600/450"),
("Steel Water Bottle","750 ml, keeps drinks cold for 24 hours.",999,"https://picsum.photos/seed/bottle/600/450")]
class Command(BaseCommand):
    def handle(self, *a, **k):
        for n,d,p,i in DATA: Product.objects.get_or_create(name=n, defaults=dict(description=d, price=p, image_url=i))
        self.stdout.write("Seeded products.")
