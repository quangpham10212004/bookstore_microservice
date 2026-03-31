from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.SerializerMethodField()
    cloth_id = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_book_id(self, obj):
        return obj.product_id if obj.product_type == "book" else None

    def get_cloth_id(self, obj):
        return obj.product_id if obj.product_type == "cloth" else None


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "customer_id", "items", "created_at", "updated_at"]


class AddToCartSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    book_id = serializers.IntegerField(required=False)
    cloth_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=False)
    product_type = serializers.ChoiceField(choices=["book", "cloth"], required=False, default="book")
    quantity = serializers.IntegerField(default=1)

    def validate(self, attrs):
        if attrs.get("book_id") is not None:
            attrs["product_type"] = "book"
            attrs["product_id"] = attrs["book_id"]
        elif attrs.get("cloth_id") is not None:
            attrs["product_type"] = "cloth"
            attrs["product_id"] = attrs["cloth_id"]
        elif attrs.get("product_id") is None:
            raise serializers.ValidationError("book_id, cloth_id hoặc product_id là bắt buộc.")
        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=False)
    cloth_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=False)
    product_type = serializers.ChoiceField(choices=["book", "cloth"], required=False, default="book")
    quantity = serializers.IntegerField(min_value=0)

    def validate(self, attrs):
        if attrs.get("book_id") is not None:
            attrs["product_type"] = "book"
            attrs["product_id"] = attrs["book_id"]
        elif attrs.get("cloth_id") is not None:
            attrs["product_type"] = "cloth"
            attrs["product_id"] = attrs["cloth_id"]
        elif attrs.get("product_id") is None:
            raise serializers.ValidationError("book_id, cloth_id hoặc product_id là bắt buộc.")
        return attrs
