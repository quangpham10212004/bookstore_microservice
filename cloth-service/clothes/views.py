from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cloth
from .serializers import ClothSerializer


class ClothViewSet(viewsets.ModelViewSet):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

    def get_queryset(self):
        queryset = Cloth.objects.all()

        catalog_id = self.request.query_params.get("catalog_id") or self.request.query_params.get("catalog")
        if catalog_id:
            queryset = queryset.filter(catalog_id=catalog_id)

        search = self.request.query_params.get("search") or self.request.query_params.get("q")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(brand__icontains=search)
                | Q(sku__icontains=search)
                | Q(description__icontains=search)
                | Q(color__icontains=search)
                | Q(material__icontains=search)
            )

        ordering = self.request.query_params.get("ordering")
        if ordering:
            allowed_fields = {
                "id",
                "name",
                "brand",
                "price",
                "stock",
                "catalog_id",
                "created_at",
                "updated_at",
            }
            order_fields = []
            for field in ordering.split(","):
                field = field.strip()
                normalized = field[1:] if field.startswith("-") else field
                if normalized in allowed_fields:
                    order_fields.append(field)
            if order_fields:
                queryset = queryset.order_by(*order_fields)

        return queryset

    @action(detail=False, methods=["get"])
    def by_catalog(self, request):
        catalog_id = request.query_params.get("catalog_id")
        if not catalog_id:
            return Response({"error": "catalog_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        clothes = Cloth.objects.filter(catalog_id=catalog_id)
        return Response(self.get_serializer(clothes, many=True).data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        q = request.query_params.get("q", "")
        clothes = Cloth.objects.filter(Q(name__icontains=q) | Q(brand__icontains=q))
        return Response(self.get_serializer(clothes, many=True).data)

    @action(detail=True, methods=["post"])
    def update_stock(self, request, pk=None):
        cloth = self.get_object()
        quantity = int(request.data.get("quantity", 0))
        cloth.stock += quantity
        if cloth.stock < 0:
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
        cloth.save()
        return Response(ClothSerializer(cloth).data)
