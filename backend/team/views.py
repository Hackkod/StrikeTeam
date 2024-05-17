from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .permissions import IsTeammate, CanCreateTeammateOrInventory

class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = [IsAuthenticated, IsTeammate]
    
    def get_queryset(self):
        user = self.request.user
        teams = Teams.objects.filter(teammates__user=user).distinct()
        return teams
    
    def perform_create(self, serializer):
        team = serializer.save()
        Teammates.objects.create(
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
    
# def logout_view(request):
#     logout(request)
#     return redirect('/')
    