from rest_framework.viewsets import ModelViewSet

from .models import (
    Building,
    BuildingRole,
    BuildingExpense,
    Unit,
    BuildingMembership, User,
)

from .serializers import (
    BuildingSerializer,
    BuildingRoleSerializer,
    BuildingExpenseSerializer,
    UnitSerializer,
    BuildingMembershipSerializer, UserSerializer,
)
from .permissions import (
    BuildingRolePermission,
    BuildingScopedPermission,
    OwnUserPermission,
)


class AuthenticatedModelViewSet(ModelViewSet):
    pass


class BuildingViewSet(AuthenticatedModelViewSet):
    serializer_class = BuildingSerializer
    permission_classes = [BuildingScopedPermission]
    permission_resource = "building"

    def get_queryset(self):
        return Building.objects.filter(
            memberships__user=self.request.user
        ).distinct()


class UnitViewSet(AuthenticatedModelViewSet):
    serializer_class = UnitSerializer
    permission_classes = [BuildingScopedPermission]
    permission_resource = "unit"

    def get_queryset(self):
        return Unit.objects.filter(
            building__memberships__user=self.request.user
        ).distinct()


class ExpenseViewSet(AuthenticatedModelViewSet):
    serializer_class = BuildingExpenseSerializer
    permission_classes = [BuildingScopedPermission]
    permission_resource = "buildingexpense"

    def get_queryset(self):
        return BuildingExpense.objects.filter(
            building__memberships__user=self.request.user
        ).distinct()


class BuildingMembershipViewSet(AuthenticatedModelViewSet):
    serializer_class = BuildingMembershipSerializer
    permission_classes = [BuildingScopedPermission]
    permission_resource = "buildingmembership"

    def get_queryset(self):
        return BuildingMembership.objects.filter(
            building__memberships__user=self.request.user
        ).distinct()


class BuildingRoleViewSet(AuthenticatedModelViewSet):
    queryset = BuildingRole.objects.all()
    serializer_class = BuildingRoleSerializer
    permission_classes = [BuildingRolePermission]


class UserViewSet(AuthenticatedModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [OwnUserPermission]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
