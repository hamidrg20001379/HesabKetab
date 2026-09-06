from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Building, BuildingMembership


# ponytail: keep the policy in one small table until roles need an admin-managed
# permission matrix; the object-level building check remains mandatory.
ROLE_PERMISSIONS = {
    "manager": {
        "building": {"view", "change"},
        "unit": {"view", "add", "change", "delete"},
        "buildingexpense": {"view", "add", "change", "delete"},
        "buildingmembership": {"view", "add", "change", "delete"},
    },
    "resident": {
        "building": {"view"},
        "unit": {"view"},
        "buildingexpense": {"view"},
        "buildingmembership": {"view"},
    },
}


def _building_for_object(obj):
    return obj if isinstance(obj, Building) else getattr(obj, "building", None)


def _membership_for(user, building):
    return (
        BuildingMembership.objects.select_related("role")
        .filter(user=user, building=building)
        .first()
    )


def _building_from_request(request):
    building_id = request.data.get("building")
    if building_id is None:
        return None
    try:
        return Building.objects.filter(pk=building_id).first()
    except (TypeError, ValueError):
        return None


def _action_permission(view):
    if view.action in {"list", "retrieve"}:
        return "view"
    if view.action == "create":
        return "add"
    if view.action in {"update", "partial_update"}:
        return "change"
    if view.action == "destroy":
        return "delete"
    return None


def _role_allows(membership, view, permission):
    if not membership or not permission:
        return False

    role = membership.role
    resource = view.permission_resource

    # An explicitly configured Django permission on a role overrides defaults.
    configured = role.permissions.filter(codename=f"{permission}_{resource}").exists()
    if role.permissions.exists():
        return configured

    return permission in ROLE_PERMISSIONS.get(role.code, {}).get(resource, set())


class BuildingScopedPermission(BasePermission):
    """Authorize resources through the user's membership in their building."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True

        permission = _action_permission(view)
        if request.method in SAFE_METHODS:
            return True

        # A normal user cannot create a Building because there is no existing
        # building membership from which ownership can be established.
        if request.data.get("building") is not None:
            building = _building_from_request(request)
            return _role_allows(
                _membership_for(request.user, building), view, permission
            )

        return view.action not in {"create"}

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        building = _building_for_object(obj)
        membership = _membership_for(request.user, building)
        return _role_allows(membership, view, _action_permission(view))


class BuildingRolePermission(BasePermission):
    """Role definitions are readable by users but writable only by staff."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.method in SAFE_METHODS or request.user.is_staff)
        )


class OwnUserPermission(BasePermission):
    """Profiles are private; account creation belongs outside this viewset."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.method in set(SAFE_METHODS) | {"PUT", "PATCH"}
        )

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk
