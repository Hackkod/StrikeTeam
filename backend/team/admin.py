from django.contrib import admin
from .models import Teams, Teammates, Inventory


class TeammatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'user', 'parent', 'rights', 'rank', 'invite_time')
    exclude = ('parentname',)


class InventoryAdmin(admin.ModelAdmin):
    # form = InventoryForm
    list_display = ('inventname', 'team', 'teammate', 'amount', 'category')
    exclude = ('teammate_name',)


admin.site.register(Teams)
admin.site.register(Teammates, TeammatesAdmin)
admin.site.register(Inventory, InventoryAdmin)
