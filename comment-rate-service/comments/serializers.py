from rest_framework import serializers
from .models import CommentRate


class CommentRateSerializer(serializers.ModelSerializer):
    book_id = serializers.SerializerMethodField()
    cloth_id = serializers.SerializerMethodField()
    content = serializers.CharField(source="comment", required=False)

    class Meta:
        model = CommentRate
        fields = "__all__"

    def get_book_id(self, obj):
        return obj.product_id if obj.product_type == "book" else None

    def get_cloth_id(self, obj):
        return obj.product_id if obj.product_type == "cloth" else None

    def validate(self, attrs):
        initial = getattr(self, "initial_data", {}) or {}
        if initial.get("book_id") is not None:
            attrs["product_type"] = "book"
            attrs["product_id"] = initial["book_id"]
        elif initial.get("cloth_id") is not None:
            attrs["product_type"] = "cloth"
            attrs["product_id"] = initial["cloth_id"]
        elif attrs.get("product_id") is None:
            raise serializers.ValidationError("book_id, cloth_id hoặc product_id là bắt buộc.")
        return attrs

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
