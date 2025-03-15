from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.apis.utils import inline_serializer
from apps.orders.models import Order
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
