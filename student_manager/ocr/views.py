from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from student_manager.uploader.services import create_invoice
from student_manager.ocr.services.pymupdf import pymupdf
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class OcrInvoiceView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pdf_url = request.data['pdf_file']
        result = pymupdf(pdf_file=pdf_url)
        create_invoice(**result, user=request.user)
        return Response({"result": result})
