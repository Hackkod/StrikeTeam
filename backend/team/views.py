from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .permissions import IsTeammate, CanCreateTeammateOrInventory

class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = [IsAuthenticated, IsTeammate]

class TeammatesViewSet(viewsets.ModelViewSet):
    queryset = Teammates.objects.all()
    serializer_class = TeammatesSerializer
    permission_classes = [IsAuthenticated, IsTeammate, CanCreateTeammateOrInventory]

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsTeammate, CanCreateTeammateOrInventory]
    
# def logout_view(request):
#     logout(request)
#     return redirect('/')
    