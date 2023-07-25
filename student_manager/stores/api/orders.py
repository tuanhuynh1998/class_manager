from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from student_manager.stores.selectors import (
    get_cart_by_id, 
    get_store_by_id, 
    get_address_by_id, 
    get_delivery_address_by_id
)
from student_manager.stores.services import create_order
from student_manager.stores.models import Order
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

class OutputOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    class InputSerializer(serializers.Serializer):
        store_id = serializers.IntegerField()
        cart_id = serializers.IntegerField()
        delivery_method = serializers.CharField(max_length=32)
        store_address_id = serializers.IntegerField()
        delivery_address_id = serializers.IntegerField()
        status = serializers.CharField(max_length=20)

    def post(self, request):
        data: dict = request.data
        store = get_store_by_id(pk=data["store_id"])
        cart = get_cart_by_id(pk=data["cart_id"])
        store_address = get_address_by_id(pk=data["store_address_id"])
        delivery_address = get_delivery_address_by_id(pk=data["delivery_address_id"])
        delivery_method = data["delivery_method"]
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = create_order(
            user=request.user, 
            store=store, 
            cart=cart,
            store_address=store_address,
            delivery_address=delivery_address,
            delivery_method=delivery_method,
            status=data["status"]
        )
        response = OutputOrderSerializer(order).data
        return Response(response)

# class UpdateOrderAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [BasicAuthentication]

#     class InputSerializer(serializers.Serializer):
#         ordering_for = serializers.CharField()
#         owner = serializers.CharField()

#     def put(self, request, id: int):
#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_date = serializer.validated_data
#         cart = get_cart_by_id(pk=id)
#         order_for = get_user_by_id(pk=validated_date["ordering_for"])
#         data = update_cart(
#             cart=cart,
#             owner=request.user,
#             ordering_for=order_for
#         )
#         response = OutputCartSerializer(data).data
#         return Response(response)
