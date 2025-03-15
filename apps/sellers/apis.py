from rest_framework import serializers
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.apis.pagination import LimitOffsetPagination, get_paginated_response
from apps.products.models import Product
from apps.orders.models import Order
from apps.accounts.permissions import IsSellerPermission
from .services import SellerService


class SellerProductListApi(APIView):
    permission_classes = [IsSellerPermission]

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class SellerProductListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "description", "price", "created_at", "updated_at")

    @extend_schema(
        responses={200: SellerProductListOutputSerializer(many=True)},
    )
    def get(self, request):
        service = SellerService()
        products = service.get_seller_products(request.user.id)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.SellerProductListOutputSerializer,
            queryset=products,
            request=request,
            view=self,
        )


class SellerOrderListApi(APIView):
    permission_classes = [IsSellerPermission]

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        status = serializers.ChoiceField(
            choices=Order.StatusChoices,
            required=False,
        )

    class SellerOrderListOutputSerializer(serializers.ModelSerializer):
        seller_total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

        class Meta:
            model = Order
            fields = ("id", "seller_total_amount", "status", "created_at")

    @extend_schema(
        responses={200: SellerOrderListOutputSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="status", type=str, location=OpenApiParameter.QUERY)
        ],
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        service = SellerService()
        orders = service.get_seller_orders(
            seller_id=request.user.id, filters=filters_serializer.validated_data
        )
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.SellerOrderListOutputSerializer,
            queryset=orders,
            request=request,
            view=self,
        )
