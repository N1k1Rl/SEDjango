from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    available = models.BooleanField(default=True)

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be a positive value.")

    def __str__(self):
        return self.name


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("In Process", "In Process"),
        ("Sent", "Sent"),
        ("Completed", "Completed"),
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE
    )
    products = models.ManyToManyField(Product)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES
    )

    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    def can_fulfill(self):
        return all(product.available for product in self.products.all())

    def __str__(self):
        return f"Order {self.id} - {self.status}"
