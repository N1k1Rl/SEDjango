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
            temp_product = Product.objects.create(name='Invalid product', price=-1.99, available=True)
            temp_product.full_clean()

    # product creation with any of the required fields missing (name, price, available)
    def test_create_product_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_missing_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='No price product', price=None, available=True)
            temp_product.full_clean()

    def test_create_product_missing_availability(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='No availability', price=1.99, available=None)
            temp_product.full_clean()

    # product creation with edge values for name length or name blank
    def test_create_product_name_too_long(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='x' * 256, price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_max_name_length(self):
        temp_product = Product.objects.create(name='x' * 255, price=10.00, available=True)
        self.assertEqual(temp_product.name, 'x' * 255)
    def test_create_product_name_empty(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=1.99, available=True)
            temp_product.full_clean()
    # product creation with edge values for price value
    def test_create_product_with_min_price(self):
        temp_product = Product.objects.create(name='Min price product', price=0.01, available=True)
        self.assertEqual(temp_product.price, 0.01)

    def test_create_product_with_max_price(self):
        temp_product = Product.objects.create(name='Max price product', price=99999.99, available=True)
        self.assertEqual(temp_product.price, 99999.99)
    # product creation with invalid price format
    def test_create_product_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Invalid price format', price=1.999, available=True)
            temp_product.full_clean()

    def test_create_product_price_with_too_many_decimals(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Too many decimals', price=1.12345, available=True)
            temp_product.full_clean()


class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(name='John Doe', address='123 Main Street')
        self.assertEqual(customer.name, 'John Doe')
        self.assertEqual(customer.address, '123 Main Street')

    def test_create_customer_missing_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='', address='123 Main Street')
            customer.full_clean()

    def test_create_customer_missing_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='John Doe', address='')
            customer.full_clean()

    def test_create_customer_name_too_long(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='x' * 101, address='123 Main Street')
            customer.full_clean()

    def test_create_customer_with_max_name_length(self):
        customer = Customer.objects.create(name='x' * 100, address='123 Main Street')
        self.assertEqual(customer.name, 'x' * 100)


    def test_create_customer_name_blank(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='', address='123 Main Street')
            customer.full_clean()

    def test_create_customer_address_blank(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='John Doe', address='')
            customer.full_clean()

class OrderModelTest(TestCase):
    def setUp(self):

        self.customer = Customer.objects.create(name='Nikola Różycka ', address='456 Street Street')


        self.product1 = Product.objects.create(name='Product 1', price=10.00, available=True)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, available=True)
        self.product3 = Product.objects.create(name='Product 3', price=15.00, available=False)

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, "New")
        self.assertIn(self.product1, order.products.all())
        self.assertIn(self.product2, order.products.all())



    def test_create_order_missing_customer(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(customer=None, status="New")
    def test_create_order_missing_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status=None)
            order.full_clean()

    def test_create_order_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status="InvalidStatus")
            order.full_clean()

    def test_calculate_total_price_with_products(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.calculate_total_price(), 30.00)

    def test_calculate_total_price_with_no_products(self):
        order = Order.objects.create(customer=self.customer, status="New")
        self.assertEqual(order.calculate_total_price(), 0.00)

    def test_can_fulfill_with_all_products_available(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.add(self.product1, self.product2)
        self.assertTrue(order.can_fulfill())

    def test_can_fulfill_with_unavailable_products(self):
        order = Order.objects.create(customer=self.customer, status="New")
        order.products.add(self.product1, self.product3)
        self.assertFalse(order.can_fulfill())