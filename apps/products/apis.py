from decimal import Decimal
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.apis.pagination import get_paginated_response, LimitOffsetPagination
from apps.apis.utils import inline_serializer
from apps.products.models import Product
from apps.products.services import ProductService
from apps.accounts.permissions import IsSellerPermission, IsOwnerPermission


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
            fields = ("id", "name", "price")

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


class ProductDetailApi(APIView):
    class ProductDetailOutputSerializer(serializers.ModelSerializer):
        seller = inline_serializer(
            name="ProductSeller",
            fields={
                "id": serializers.IntegerField(),
                "email": serializers.EmailField(),
            },
        )

        class Meta:
            model = Product
            fields = ("id", "name", "description", "price", "seller")

    @extend_schema(
        responses={200: ProductDetailOutputSerializer},
    )
    def get(self, request, product_id):
        service = ProductService()
        product = service.get_product_by_id(product_id=product_id)

        return Response(
            self.ProductDetailOutputSerializer(product).data, status=status.HTTP_200_OK
        )


class ProductUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    class ProductUpdateInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(allow_blank=True, required=False)
        price = serializers.DecimalField(
            max_digits=10, decimal_places=2, min_value=Decimal("0.0"), required=False
        )

    class ProductUpdateOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "price")

    @extend_schema(
        request=ProductUpdateInputSerializer,
        responses={200: ProductUpdateOutputSerializer},
    )
    def patch(self, request, product_id):
        serializer = self.ProductUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ProductService()
        product = service.get_product_by_id(product_id=product_id)
        self.check_object_permissions(request, product)
        product = service.update_product(product=product, **serializer.validated_data)

        return Response(
            self.ProductUpdateOutputSerializer(product).data, status=status.HTTP_200_OK
        )


class ProductDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    @extend_schema(
        responses={204: None},
    )
    def delete(self, request, product_id):
        service = ProductService()
        product = service.get_product_by_id(product_id=product_id)
        self.check_object_permissions(request, product)
        service.delete_product(product)

        return Response(status=status.HTTP_204_NO_CONTENT)
