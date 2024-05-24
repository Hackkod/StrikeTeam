from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from team.views import *

router = DefaultRouter()
router.register(r'teams', TeamsViewSet)
router.register(r'teammates', TeammatesViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = [
    # JWT аутентификация
    path('api/register/', register, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # стандарт. аутентификация для теста на бэкэнде
    path('api/drf-auth/', include('rest_framework.urls')),
    # Main
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/user/', UserDetailView.as_view(), name='user-detail'),
    # path('api/user/delete/', UserDetailView.as_view(), name='delete-user'),
    path('api/user/delete/', DeleteUserView, name='delete-user'),
    # path('admin/logout/', logout_view, name='logout'),
]
