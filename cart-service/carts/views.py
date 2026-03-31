import os
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer, UpdateCartItemSerializer

BOOK_SERVICE_URL = os.environ.get("BOOK_SERVICE_URL", "http://book-service:8000")
CLOTH_SERVICE_URL = os.environ.get("CLOTH_SERVICE_URL", "http://cloth-service:8000")


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def _service_url_for_item(self, product_type):
        return BOOK_SERVICE_URL if product_type == "book" else CLOTH_SERVICE_URL

    def _resource_path_for_item(self, product_type):
        return "books" if product_type == "book" else "clothes"

    @action(detail=False, methods=["get"])
    def by_customer(self, request):
        """Get cart by customer_id."""
        customer_id = request.query_params.get("customer_id")
        if not customer_id:
            return Response({"error": "customer_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(customer_id=customer_id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        # Enrich items with product details
        cart_data = CartSerializer(cart).data
        for item in cart_data["items"]:
            try:
                resource = self._resource_path_for_item(item["product_type"])
                service_url = self._service_url_for_item(item["product_type"])
                resp = requests.get(f"{service_url}/api/{resource}/{item['product_id']}/", timeout=5)
                if resp.status_code == 200:
                    product = resp.json()
                    item["product"] = product
                    item[item["product_type"]] = product
            except requests.RequestException:
                item["product"] = None
                item[item["product_type"]] = None
        return Response(cart_data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        """Add a product to the customer's cart."""
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_id = serializer.validated_data["customer_id"]
        product_type = serializer.validated_data["product_type"]
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_type=product_type,
            product_id=product_id,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"])
    def update_item(self, request):
        """Update quantity of a cart item. Quantity 0 removes the item."""
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_id = request.data.get("customer_id")
        product_type = serializer.validated_data["product_type"]
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            item = CartItem.objects.get(cart=cart, product_type=product_type, product_id=product_id)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["delete"])
    def remove_item(self, request):
        """Remove a product from the cart."""
        customer_id = request.query_params.get("customer_id")
        product_type = request.query_params.get("product_type", "book")
        product_id = request.query_params.get("product_id") or request.query_params.get("book_id") or request.query_params.get("cloth_id")
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            item = CartItem.objects.get(cart=cart, product_type=product_type, product_id=product_id)
            item.delete()
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        """Clear all items from a cart."""
        customer_id = request.query_params.get("customer_id")
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            cart.items.all().delete()
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CartSerializer(cart).data)
