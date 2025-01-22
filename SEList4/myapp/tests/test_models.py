from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Invalid product', price=-1.99, available=True)
            temp_product.full_clean()

    def test_create_product_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_missing_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='No price product', price=None, available=True)
            temp_product.full_clean()

    def test_create_product_name_too_long(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='x' * 256, price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_min_price(self):
        temp_product = Product.objects.create(name='Min price product', price=0.01, available=True)
        self.assertEqual(temp_product.price, 0.01)
