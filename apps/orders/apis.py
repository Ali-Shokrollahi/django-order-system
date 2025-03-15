from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.accounts.permissions import IsOwnerPermission
from apps.apis.utils import inline_serializer
from apps.orders.models import Order, OrderItem
from apps.orders.services import OrderService


class OrderCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    class OrderCreateInputSerializer(serializers.Serializer):
        products_data = inline_serializer(
            name="ProductOrderDataSerializer",
            fields={
                "product_id": serializers.UUIDField(),
                "quantity": serializers.IntegerField(min_value=1),
            },
            many=True,
            allow_empty=False,
        )

    class OrderCreateOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ("id", "total_amount", "status", "created_at")

    @extend_schema(
        request=OrderCreateInputSerializer,
        responses={201: OrderCreateOutputSerializer},
    )
    def post(self, request):
        serializer = self.OrderCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = OrderService()

        order = service.create_order(
            customer=request.user,
            products_data=serializer.validated_data["products_data"],
        )

        return Response(
            self.OrderCreateOutputSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderListApi(APIView):
    permission_classes = [IsAuthenticated]

    class FilterSerializer(serializers.Serializer):
        status = serializers.ChoiceField(
            choices=Order.StatusChoices,
            required=False,
        )

    class OrderListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ("id", "total_amount", "status", "created_at")

    @extend_schema(
        responses={200: OrderListOutputSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="status", type=str, location=OpenApiParameter.QUERY)
        ],
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        service = OrderService()
        orders = service.get_customer_orders(
            customer_id=request.user.id, filters=filters_serializer.validated_data
        )

        return Response(self.OrderListOutputSerializer(orders, many=True).data)


class OrderItemSerializer(serializers.ModelSerializer):
    product_total_amount = serializers.SerializerMethodField(
        method_name="get_product_total_amount"
    )
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = OrderItem
        fields = ("product_name", "quantity", "product_total_amount")

    def get_product_total_amount(self, obj):
        return obj.product.price * obj.quantity


class OrderDetailApi(APIView):
    owner_field = "customer"
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    class OrderDetailOutputSerializer(serializers.ModelSerializer):
        order_items = OrderItemSerializer(many=True, source="orderitem_set")

        class Meta:
            model = Order
            fields = ("id", "total_amount", "status", "created_at", "order_items")

    @extend_schema(
        responses={200: OrderDetailOutputSerializer},
    )
    def get(self, request, order_id):
        service = OrderService()
        order = service.get_order_details(order_id)
        self.check_object_permissions(request, order)

        return Response(self.OrderDetailOutputSerializer(order).data)
