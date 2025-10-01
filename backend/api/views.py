from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice
from .serializers import InvoiceSerializer
from .utils import extract_text_from_pdf, extract_invoice_data  # your own logic
from datetime import datetime

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def get_queryset(self):
        user= self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author= self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        return Note.objects.filter(author=user)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class InvoiceUploadAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        file = request.FILES.get('pdf')  # 'pdf' is the key used in FormData from React
        if not file:
            return Response({"error": "No PDF file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        invoice = Invoice.objects.create(file=file)

        try:
            text = extract_text_from_pdf(invoice.file.path)
            extracted_data = extract_invoice_data(text)
            print(extracted_data)
            invoice.invoice_number = extracted_data.get('invoice_number')
            invoice.amount = extracted_data.get('amount')

            try:
                invoice.invoice_date = datetime.strptime(extracted_data.get('invoice_date', ''), '%Y-%m-%d').date()
            except Exception as e:
                print("Date parse error:", e)

            try:
                invoice.due_date = datetime.strptime(extracted_data.get('due_date', ''), '%Y-%m-%d').date()
            except Exception as e:
                print("Due date parse error:", e)
            
            invoice.invoice_date= extracted_data.get('invoice_date')
            invoice.due_date= extracted_data.get('due_date')
            invoice.extracted = True
            invoice.save()

            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to extract PDF: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)