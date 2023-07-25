from django.http import HttpRequest
from .models import Subject
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateSubjectSerializer, DetailsSubjectSerializer, DeleteSubjectSerializer
from rest_framework.authentication import BasicAuthentication
from commons.exceptions import NotFoundException, ValidationException
from rest_framework.generics import ListAPIView
from commons.middlewares.pagination import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated

class CreateSubjectView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        data: dict = request.data
        serializer_data = CreateSubjectSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

class GetAndUpdateAndDeleteSubjectView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, subject_id: int):
        data = Subject.objects.filter(pk=subject_id)
        if not data.exists():
            raise NotFoundException
        serializer_data = DetailsSubjectSerializer(data.first())
        return Response(serializer_data.data)

    def put(self, request: HttpRequest, subject_id: int):
        data: dict = request.data
        subject = Subject.objects.filter(pk=subject_id)
        if not subject.exists():
            raise NotFoundException
        serializer_data = DetailsSubjectSerializer(subject.first(), data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

    def delete(self, request: HttpRequest, subject_id: int):
        subject = Subject.objects.filter(pk=subject_id)
        if not subject.exists():
            raise NotFoundException
        serializer_data = DeleteSubjectSerializer(subject.first(), data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({})
        else:
            raise ValidationException(data=serializer_data.errors)

class ListSubjectView(ListAPIView):
    serializer_class = DetailsSubjectSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):        
        data: dict = self.request.GET
        queryset = Subject.objects.filter(name__icontains=data['name']).order_by('id')
        return queryset
 