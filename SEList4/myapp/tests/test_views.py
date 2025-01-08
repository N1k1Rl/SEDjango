from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from myapp.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class ProductApiTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Temporary Product', price=1.99, available=True
        )
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})
        self.client = APIClient()
        self.regular_user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.admin = User.objects.create_superuser(
            username='testadmin', password='testpassword'
        )

    def test_regular_user_get_all_products(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_products(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary Product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_regular_user_create_product(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_product(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Temporary Product 2')
        self.assertEqual(response.data['price'], '4.99')
        self.assertTrue(response.data['available'])

    def test_regular_user_delete_product(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_delete_product(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_invalid_data(self):
        data = {"name": "", "price": -1, "available": None}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

