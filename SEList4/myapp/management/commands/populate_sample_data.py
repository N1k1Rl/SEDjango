from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()


        product1 = Product.objects.create(
            name="1989 (Taylor's Version) - Taylor Swift Vinyl",
            price=39.99,
            available=True
        )
        product2 = Product.objects.create(
            name="Folklore - Taylor Swift Vinyl",
            price=49.99,
            available=True
        )
        product3 = Product.objects.create(
            name="The Tortured Poets Department - Taylor Swift Vinyl",
            price=59.99,
            available=False
        )


        customer1 = Customer.objects.create(
            name="Krystian Górny",
            address="Stanisława Drabika 73/7"
                    "52-131 Wrocław"
        )
        customer2 = Customer.objects.create(
            name="Nikola Różycka",
            address="Emilii Plater 5/10"
                    "97-300 Piotrków Trybunalski"
        )

        customer3 = Customer.objects.create(
            name="Maja Adamusiak",
            address="Słowackiego 90"
                    "97-300 Piotrków Trybunalski"
        )

        order1 = Order.objects.create(
            customer=customer1,
            status="New"
        )
        order2 = Order.objects.create(
            customer=customer2,
            status="In Process"
        )
        order3 = Order.objects.create(
            customer=customer3,
            status="Sent"
        )

        order1.products.add(product1, product2)
        order2.products.add(product2, product3)
        order3.products.add(product1)

        self.stdout.write("Data created successfully.")
