from django.http import HttpRequest
from commons.exceptions import NotFoundException, ValidationException
from .models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateStudentSerializer, DetailsStudentSerializer, DeleteStudentSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListAPIView
from commons.middlewares.pagination import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated

class CreateStudentView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        data: dict = request.data
        serializer_data = CreateStudentSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

class GetAndUpdateAndDeleteStudentView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, student_id: int):
        data = Student.objects.filter(pk=student_id)
        if not data.exists():
            raise NotFoundException
        return Response(DetailsStudentSerializer(data.first()).data)
    
    def put(self, request: HttpRequest, student_id: int):
        data: dict = request.data
        student = Student.objects.filter(pk=student_id)
        if not student.exists():
            raise NotFoundException
        serializer_data = DetailsStudentSerializer(student.first(), data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

    def delete(self, request: HttpRequest, student_id: int):
        student = Student.objects.filter(pk=student_id)
        if not student.exists():
            raise NotFoundException
        serializer_data = DeleteStudentSerializer(student.first(), data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({})
        else:
            raise ValidationException(data=serializer_data.errors)

class ListStudentView(ListAPIView):
    serializer_class = DetailsStudentSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):        
        data: dict = self.request.GET
        queryset = Student.objects.filter(name__icontains=data['name']).order_by('id')
        return queryset
