from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from commons.middlewares.pagination import StandardResultsSetPagination
from student_manager.stores.selectors import list_product
from student_manager.stores.services import create_product
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

class DetailProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    brand = serializers.CharField()
    description = serializers.CharField()
    average_cost = serializers.DecimalField(max_digits=19, decimal_places=4, default=0)
    status = serializers.CharField()
    sellable = serializers.BooleanField()

class ListProductAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    serializer_class = DetailProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        data: dict = self.request.GET
        query_dict = dict((k, v) for k, v in data.items() if v)
        queryset = list_product(filter=query_dict)
        return queryset

class CreateProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        data: dict = request.data
        serializer = DetailProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        create_product(**serializer.validated_data)
        return Response({"message": "success"})
