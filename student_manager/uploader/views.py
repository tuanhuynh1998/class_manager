from io import BytesIO
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import PublicS3MediaStorage, file_upload
from rest_framework.views import APIView
from django.core.files import File
from django.views.generic import TemplateView
from student_manager.users.models import User
from rest_framework.permissions import IsAuthenticated

@api_view(('POST',))
def save_file(request):
    file_name = "sample1.txt"
    file_content = b"Sample text file"
    file_content_io = BytesIO(file_content)

    storage = PublicS3MediaStorage()
    storage.save(file_name, file_content_io)
    return Response({"message": storage.url(file_name)})

class UploadFile(APIView):
    def post(self, request):
        file = request.FILES['image_file']
        converted_file = File(file, file.name)
        file_url = file_upload(converted_file)
        return Response({"message": file_url})

class InvoiceView(TemplateView):
    template_name = "invoice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=kwargs['pk'])
        return context
