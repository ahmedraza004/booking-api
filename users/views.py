from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, SignupSerializer
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
