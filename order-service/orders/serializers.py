from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    book_id = serializers.SerializerMethodField()
    cloth_id = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_book_id(self, obj):
        return obj.product_id if obj.product_type == "book" else None

    def get_cloth_id(self, obj):
        return obj.product_id if obj.product_type == "cloth" else None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class CreateOrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    payment_method = serializers.CharField(max_length=50)
    shipping_method = serializers.CharField(max_length=50)
    shipping_address = serializers.CharField()
