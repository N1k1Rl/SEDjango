from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal

# Create your views here.
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hello, World!")


@csrf_exempt
def product_list(request):
    if request.method == "GET":
        products = list(Product.objects.values("id", "name", "price", "available"))
        return JsonResponse(products, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            price = data.get("price")
            available = data.get("available")

            if not name or not price or available is None:
                return HttpResponseBadRequest("Missing one of the fields: 'name', 'price', or 'available'.")

            if float(price) < 0:
                return HttpResponseBadRequest("Price has to be greater than 0.")

            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()

            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "available": product.available
            }, status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")

        except Exception as e:
            return HttpResponseBadRequest(str(e))

    else:
        return HttpResponseBadRequest("Method not available.")


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)

        if request.method == "GET":
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "available": product.available
            })

        else:
            return HttpResponseNotAllowed(["GET"])

    except Product.DoesNotExist:
        return HttpResponseNotFound(f"Product with ID {product_id} doesn't exist.")
