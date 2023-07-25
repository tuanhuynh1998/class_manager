from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from commons.middlewares.pagination import StandardResultsSetPagination
from student_manager.stores.services import create_store
from student_manager.stores.selectors import get_list_store
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

class DetailStoreSerializer(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.ImageField(required=False, allow_null=True)
    url = serializers.CharField()
    email = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField()
    city = serializers.CharField()
    province = serializers.CharField()
    landmark = serializers.CharField()
    latitude = serializers.IntegerField()
    longitude = serializers.IntegerField()
    active = serializers.BooleanField()
    user_id = serializers.IntegerField()

class CreateStoreAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        image = serializers.ImageField(required=False, allow_null=True)
        url = serializers.CharField()
        email = serializers.CharField(required=False, allow_null=True)
        address = serializers.CharField()
        city = serializers.CharField()
        province = serializers.CharField()
        landmark = serializers.CharField()
        latitude = serializers.IntegerField()
        longitude = serializers.IntegerField()

    def post(self, request):
        current_user = request.user
        request.data['image'] = request.FILES["image"]
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = create_store(user=current_user, **serializer.validated_data)
        response = DetailStoreSerializer(store)
        return Response(response.data)

class ListStoreAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    serializer_class = DetailStoreSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        data: dict = self.request.GET
        queryset = get_list_store(name=data["name"])
        return queryset
