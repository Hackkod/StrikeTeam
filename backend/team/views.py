from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .permissions import IsTeammate, CanCreateTeammateOrInventory

class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsTeammate]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        teams = Teams.objects.filter(teammates__user=user).distinct()
        return teams
    
    def perform_create(self, serializer):
        team = serializer.save()
        # Отключение проверок разрешений для создания тиммейта
        self.request.user.teammates_set.create(
            team=team,
            user=self.request.user,
            name=self.request.user.username,
            rights='admin'
        )

class TeammatesViewSet(viewsets.ModelViewSet):
    queryset = Teammates.objects.all()
    serializer_class = TeammatesSerializer
    permission_classes = [IsAuthenticated, IsTeammate, CanCreateTeammateOrInventory]
    
    def get_queryset(self):
        user = self.request.user
        teammates = Teammates.objects.filter(team__teammates__user=user).distinct()
        return teammates

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsTeammate, CanCreateTeammateOrInventory]
    
    def get_queryset(self):
        user = self.request.user
        inventory = Inventory.objects.filter(team__teammates__user=user).distinct()
        return inventory
    
    def perform_create(self, serializer):
        team = self.request.data.get('team')
        if team:
            team = Teams.objects.get(id=team)
        serializer.save(team=team)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    try:
        user = User.objects.create(
            username=username,
            password=make_password(password)
        )
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# def logout_view(request):
#     logout(request)
#     return redirect('/')
    