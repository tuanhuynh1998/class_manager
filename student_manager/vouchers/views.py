from django.http import HttpRequest
from commons.middlewares.pagination import StandardResultsSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .services import create_voucher
from .selectors import voucher_available_to_user

class VoucherDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    user_limit = serializers.IntegerField()
    max_redemption = serializers.IntegerField()
    valid_until = serializers.DateTimeField()
    promo_type = serializers.CharField()
    discount_value = serializers.IntegerField()
    minimum_order_amount = serializers.IntegerField()
    min_order_count = serializers.IntegerField()
    max_order_count = serializers.IntegerField()
    exclusive_to_user = serializers.BooleanField(default=True)
    active = serializers.BooleanField(default=True)
    claimable = serializers.BooleanField(default=True)

class CreateVoucherAPIView(APIView):
    class CreateVoucherSerializer(serializers.Serializer):
        name = serializers.CharField()
        code = serializers.CharField()
        user_limit = serializers.IntegerField()
        max_redemption = serializers.IntegerField()
        promo_type = serializers.CharField()
        discount_value = serializers.IntegerField()
        minimum_order_amount = serializers.IntegerField()
        min_order_count = serializers.IntegerField()
        max_order_count = serializers.IntegerField()
        exclusive_to_user = serializers.BooleanField(default=True)
        active = serializers.BooleanField(default=True)
        claimable = serializers.BooleanField(default=True)

    def post(self, request: HttpRequest):
        data: dict = request.data
        serializer = self.CreateVoucherSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        voucher = create_voucher(**serializer.validated_data)
        return Response(VoucherDetailSerializer(voucher).data)

class ListVoucherAvailableToView(ListAPIView):
    serializer_class = VoucherDetailSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = voucher_available_to_user(user=self.request.user)
        return queryset
