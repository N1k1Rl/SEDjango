from django.urls import path
from .views import hello_world
from .views import ProductListView, ProductDetailView, ProductCreateView
urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path("user/products/", ProductListView.as_view(),
                    name="product_list"),
    path("user/products/<int:pk>/", ProductDetailView.as_view(),
                    name="product_detail"),
    path("user/products/new/", ProductCreateView.as_view(),
                    name="product_create"),
]
