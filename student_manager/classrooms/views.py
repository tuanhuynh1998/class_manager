from django.http import HttpRequest
from commons.exceptions import NotFoundException, ValidationException
from commons.middlewares.pagination import StandardResultsSetPagination
from .serializers import CreateClassRoomSerializer, DetailsClassRoomSerializer, DeleteClassRoomSerializer
from .models import ClassRoom
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class CreateClassRoomView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        data: dict = request.data
        serializer_data = CreateClassRoomSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

class ListClassRoomView(ListAPIView):
    serializer_class = DetailsClassRoomSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data: dict = self.request.GET
        queryset = ClassRoom.objects.filter(name__icontains=data['name']).order_by('id')
        return queryset

class GetAndUpdateAndDeleteClassRoomView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, class_room_id: int):
        data = ClassRoom.objects.filter(pk=class_room_id).first()
        if data is None:
            raise NotFoundException
        response = DetailsClassRoomSerializer(data)
        return Response(response.data)

    def put(self, request: HttpRequest, class_room_id: int):
        data: dict = request.data
        classroom = ClassRoom.objects.filter(pk=class_room_id).first()
        if classroom is None:
            raise NotFoundException
        serializer_data = DetailsClassRoomSerializer(classroom, data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

    def delete(self, request: HttpRequest, class_room_id: int):
        data = ClassRoom.objects.filter(pk=class_room_id)
        if not data.exists():
            raise NotFoundException
        serializer_data = DeleteClassRoomSerializer(data.first(), data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({})
        else:
            raise ValidationException(data=serializer_data.errors)
