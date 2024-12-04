from django.urls import path
from .views import hello_world
from .views import product_list, product_detail

urlpatterns = [
path('hello/', hello_world, name='hello_world'),
path('api/products/', product_list, name = "product_list"),
path('api/products/<int:product_id>/', product_detail, name="product detail"),]
