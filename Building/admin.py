from django.contrib import admin
from .models import Building,Unit,BuildingExpense,BuildingMembership,BuildingRole

from Building.models import User

admin.site.register(Building)
admin.site.register(BuildingRole)
admin.site.register(BuildingExpense)
admin.site.register(BuildingMembership)
admin.site.register(Unit)
