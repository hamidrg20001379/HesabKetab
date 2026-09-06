from rest_framework.serializers import ModelSerializer

from .models import User, Building, BuildingRole, BuildingExpense, Unit, BuildingMembership


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "telegram_chat_id",
        ]

class BuildingSerializer(ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class BuildingRoleSerializer(ModelSerializer):
    class Meta:
        model = BuildingRole
        fields = '__all__'

class BuildingExpenseSerializer(ModelSerializer):
    class Meta:
        model = BuildingExpense
        fields = '__all__'

class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class BuildingMembershipSerializer(ModelSerializer):
    class Meta:
        model = BuildingMembership
        fields = '__all__'



