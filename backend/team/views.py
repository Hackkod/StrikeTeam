from djoser.conf import User
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from .models import Teams, Teammates, Inventory
from .serializers import TeamsSerializer, TeammatesSerializer, InventorySerializer, UserSerializer
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
        teams = Teams.objects.filter(
            teammates__user=user
        ).distinct()
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
        queryset = Teammates.objects.filter(
            team__teammates__user=user
        ).distinct()
        team_id = self.request.query_params.get('team')
        if team_id:
            queryset = queryset.filter(
                team_id=team_id
            )
        return queryset


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsTeammate, CanCreateTeammateOrInventory]

    def get_queryset(self):
        user = self.request.user
        inventory = Inventory.objects.filter(
            team__teammates__user=user
        ).distinct()
        return inventory

    def perform_create(self, serializer):
        self.custom_save(serializer, self.request.data)

    def perform_update(self, serializer):
        self.custom_save(serializer, self.request.data, update=True)

    def custom_save(self, serializer, data, update=False):
        team = data.get('team')
        teammate = data.get('teammate')
        inventname = data.get('inventname')
        amount = data.get('amount')

        team_instance = Teams.objects.get(id=team)
        teammate_instance = Teammates.objects.get(id=teammate) if teammate else None

        existing_inventory = Inventory.objects.filter(
            team=team_instance,
            teammate=teammate_instance,
            inventname=inventname
        ).first()

        if existing_inventory:
            if update:
                if existing_inventory.id != serializer.instance.id:
                    existing_inventory.amount += int(amount)
                    existing_inventory.save()
                    serializer.instance.delete()
                    serializer.instance = existing_inventory
                else:
                    existing_inventory.amount = int(amount)
                    existing_inventory.save()
            else:
                existing_inventory.amount += int(amount)
                existing_inventory.save()
                serializer.instance = existing_inventory
        else:
            inventory = serializer.save(
                team=team_instance,
                teammate=teammate_instance
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def categories(self, request):
        categories = Inventory.CATEGORIES
        return Response(categories)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


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

