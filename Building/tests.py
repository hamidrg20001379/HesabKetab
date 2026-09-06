from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Building, BuildingMembership, BuildingRole, Unit, User


class BuildingRoleAuthorizationTests(APITestCase):
    def setUp(self):
        self.manager_role = BuildingRole.objects.create(code="manager", name_en="Manager")
        self.resident_role = BuildingRole.objects.create(code="resident", name_en="Resident")
        self.manager = User.objects.create_user(username="manager", password="test-pass")
        self.resident = User.objects.create_user(username="resident", password="test-pass")
        self.other_manager = User.objects.create_user(username="other", password="test-pass")
        self.building = Building.objects.create(name="First", code="first")
        self.other_building = Building.objects.create(name="Second", code="second")
        BuildingMembership.objects.create(
            user=self.manager, building=self.building, role=self.manager_role
        )
        BuildingMembership.objects.create(
            user=self.resident, building=self.building, role=self.resident_role
        )
        BuildingMembership.objects.create(
            user=self.other_manager, building=self.other_building, role=self.manager_role
        )
        self.unit = Unit.objects.create(building=self.building, number=1)
        self.other_unit = Unit.objects.create(building=self.other_building, number=1)

    def test_resident_can_read_but_cannot_mutate_units(self):
        self.client.force_authenticate(self.resident)

        response = self.client.get(reverse("unit-list"))
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(
            reverse("unit-detail", args=[self.unit.pk]), {"number": 2}, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_can_mutate_only_units_in_their_building(self):
        self.client.force_authenticate(self.manager)

        response = self.client.patch(
            reverse("unit-detail", args=[self.unit.pk]), {"number": 2}, format="json"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(
            reverse("unit-detail", args=[self.other_unit.pk]), {"number": 2}, format="json"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            reverse("unit-list"), {"building": self.other_building.pk, "number": 2}, format="json"
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.post(
            reverse("unit-list"), {"building": "not-an-id", "number": 3}, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_role_catalog_is_not_writable_by_building_members(self):
        self.client.force_authenticate(self.resident)

        response = self.client.post(
            reverse("building-role-list"), {"code": "auditor"}, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_user_viewset_exposes_only_the_current_profile(self):
        self.client.force_authenticate(self.resident)

        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.resident.pk)

        response = self.client.get(reverse("user-detail", args=[self.manager.pk]))
        self.assertEqual(response.status_code, 404)
