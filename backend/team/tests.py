from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Teams, Teammates, Inventory


class TeamsModelTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Создаем команду
        self.team = Teams.objects.create(teamname='Test Team')

        # Создаем тиммейта
        self.teammate = Teammates.objects.create(
            team=self.team,
            user=self.user,
            name='Teammate 1',
            rights='admin'
        )

        # Создаем инвентарь
        self.inventory = Inventory.objects.create(
            team=self.team,
            teammate=self.teammate,
            inventname='Test Inventory',
            amount=10,
            category='Привода'
        )

    def test_team_creation(self):
        """Тест создания команды"""
        team = Teams.objects.get(teamname='Test Team')
        self.assertEqual(team.teamname, 'Test Team')

    def test_teammate_creation(self):
        """Тест создания тиммейта"""
        teammate = Teammates.objects.get(name='Teammate 1')
        self.assertEqual(teammate.name, 'Teammate 1')
        self.assertEqual(teammate.user.username, 'testuser')

    def test_inventory_creation(self):
        """Тест создания инвентаря"""
        inventory = Inventory.objects.get(inventname='Test Inventory')
        self.assertEqual(inventory.inventname, 'Test Inventory')
        self.assertEqual(inventory.amount, 10)
        self.assertEqual(inventory.category, 'Привода')

    def test_inventory_teammate_name(self):
        """Тест правильного сохранения имени тиммейта в инвентаре"""
        inventory = Inventory.objects.get(inventname='Test Inventory')
        self.assertEqual(inventory.teammate_name, 'Teammate 1')

    def test_inventory_default_teammate_name(self):
        """Тест правильного сохранения имени 'Команда' в инвентаре при отсутствии тиммейта"""
        inventory = Inventory.objects.create(
            team=self.team,
            inventname='Team Inventory',
            amount=5,
            category='Продовольствие'
        )
        self.assertEqual(inventory.teammate_name, 'Команда')


class TeamsAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.team = Teams.objects.create(teamname='Test Team')
        self.teammate = Teammates.objects.create(
            team=self.team,
            user=self.user,
            name='Teammate 1',
            rights='admin'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_teams(self):
        """Тест получения списка команд"""
        response = self.client.get(reverse('teams-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['teamname'], 'Test Team')
