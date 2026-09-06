from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    BuildingViewSet,
    BuildingRoleViewSet,
    ExpenseViewSet,
    UnitViewSet,
    BuildingMembershipViewSet,
)


router = DefaultRouter()

router.register("users", UserViewSet, basename="user")
router.register("buildings", BuildingViewSet, basename="building")
router.register("roles", BuildingRoleViewSet, basename="building-role")
router.register("expenses", ExpenseViewSet, basename="building-expense")
router.register("units", UnitViewSet, basename="unit")
router.register("memberships", BuildingMembershipViewSet, basename="building-membership")


urlpatterns = [
    path("", include(router.urls)),
]
