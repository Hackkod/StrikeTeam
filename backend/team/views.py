from rest_framework import generics
# from django.shortcuts import render
# from django.forms import model_to_dict

from .models import *
from .serializers import *
# from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

class TeamsAPIList(generics.ListCreateAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

class TeamsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer  
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

class TeamsAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer 
    # permission_classes = (IsAdminOrReadOnly,) 
    