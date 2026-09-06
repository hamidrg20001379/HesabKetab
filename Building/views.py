from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Building, BuildingRole, BuildingExpense, Unit, BuildingMembership
from .serializers import (
    BuildingSerializer,
    BuildingRoleSerializer,
    BuildingExpenseSerializer,
    UnitSerializer,
    BuildingMembershipSerializer,
)


class BuildingViewSet(ModelViewSet):
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Building.objects.filter(
            memberships__user=self.request.user
        ).distinct()


class UnitViewSet(ModelViewSet):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Unit.objects.filter(
            building__memberships__user=self.request.user
        ).distinct()


class ExpenseViewSet(ModelViewSet):
    serializer_class = BuildingExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BuildingExpense.objects.filter(
            building__memberships__user=self.request.user
        ).distinct()


class BuildingMembershipViewSet(ModelViewSet):
    serializer_class = BuildingMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BuildingMembership.objects.filter(
            building__memberships__user=self.request.user
        ).distinct()


class BuildingRoleViewSet(ModelViewSet):
    queryset = BuildingRole.objects.all()
    serializer_class = BuildingRoleSerializer
    permission_classes = [IsAuthenticated]