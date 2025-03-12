from decimal import Decimal
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.apis.pagination import get_paginated_response, LimitOffsetPagination
from apps.products.models import Product
from apps.products.services import ProductService
from apps.accounts.permissions import IsSellerPermission


class ProductCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsSellerPermission]

    class ProductCreateInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        description = serializers.CharField(allow_blank=True, required=False)
        price = serializers.DecimalField(
            max_digits=10, decimal_places=2, min_value=Decimal("0.0")
        )

    class ProductCreateOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "price", "seller")

    @extend_schema(
        request=ProductCreateInputSerializer,
        responses={201: ProductCreateOutputSerializer},
    )
    def post(self, request):
        serializer = self.ProductCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ProductService()
        product = service.create_product(
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description"),
            price=serializer.validated_data["price"],
            seller=request.user,
        )

        return Response(
            self.ProductCreateOutputSerializer(product).data,
            status=status.HTTP_201_CREATED,
        )


class ProductListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        search = serializers.CharField(max_length=255, required=False)
        price_min = serializers.DecimalField(
            max_digits=10, decimal_places=2, min_value=Decimal("0.0"), required=False
        )
        price_max = serializers.DecimalField(
            max_digits=10, decimal_places=2, min_value=Decimal("0.0"), required=False
        )
        seller = serializers.IntegerField(required=False, min_value=1)

    class ProductListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "price", "seller")

    @extend_schema(
        responses=ProductListOutputSerializer(many=True),
        parameters=[
            OpenApiParameter(name="search", type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(
                name="price_min", type=Decimal, location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name="price_max", type=Decimal, location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(name="seller", type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="limit", type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="offset", type=int, location=OpenApiParameter.QUERY),
        ],
    )
    def get(self, request):
        service = ProductService()
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        products = service.get_all_products(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.ProductListOutputSerializer,
            queryset=products,
            request=request,
            view=self,
        )
