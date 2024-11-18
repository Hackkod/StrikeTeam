from rest_framework import permissions
from .models import Teams, Teammates, Inventory


class IsTeammate(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return Teammates.objects.filter(user=user).exists()

    def has_object_permission(self, request, view, obj):
        user = request.user
        team_id = None

        # Определяем команду в зависимости от типа объекта
        if isinstance(obj, Teams):
            team_id = obj.id
        elif isinstance(obj, Teammates) or isinstance(obj, Inventory):
            team_id = obj.team.id

        # Проверяем, есть ли у пользователя права в этой команде
        teammate = Teammates.objects.filter(user=user, team_id=team_id).first()
        if not teammate:
            return False

        # Администраторы имеют полный доступ
        if teammate.rights == 'admin':
            return True

        # Чтение данных для тиммейтов
        if request.method in permissions.SAFE_METHODS:
            return True

        # Редактирование инвентаря для тиммейтов с правами editor
        if teammate.rights == 'editor':
            if isinstance(obj, Inventory):
                return True

        return False

    
class CanCreateTeammateOrInventory(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        teammate = Teammates.objects.filter(user=user).first()
        
        if not teammate:
            return False
        
        # Только админы и редакторы могут создавать тиммейтов и инвентарь
        if request.method == 'POST':
            if teammate.rights == 'admin':
                return True
            if teammate.rights == 'editor':
                if view.basename == 'inventory':
                    return True
            return False
        
        return True

# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_permissions(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         return bool(request.user and request.user.is_staff)

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return obj.user == request.user