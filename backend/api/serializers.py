from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Invoice
import os


#Serializer-> TAKES python obj and converts to JSON data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)  # ** unpack a dic to kwargs
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}

class InvoiceSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "filename",
            "invoice_date",
            "invoice_number",
            "amount",
            "due_date",
            "extracted",
        ]

    def get_filename(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)
        return None
