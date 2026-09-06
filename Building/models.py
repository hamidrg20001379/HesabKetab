from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils import timezone

import jdatetime


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="شماره همراه",
    )

    payment_card_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        verbose_name="شماره کارت جهت واریز شارژ",
    )

    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="آیدی تلگرام",
    )

    def __str__(self):
        return self.get_full_name() or self.username


class Building(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="نام ساختمان",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="کد ساختمان",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ساختمان"
        verbose_name_plural = "ساختمان‌ها"


class BuildingRole(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="کد نقش",
    )

    name_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام انگلیسی",
    )

    name_fa = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام فارسی",
    )

    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="building_roles",
    )

    def __str__(self):
        return self.name_fa or self.name_en or self.code

    class Meta:
        verbose_name = "نقش ساختمان"
        verbose_name_plural = "نقش‌های ساختمان"


class BuildingMembership(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="building_memberships",
        verbose_name="کاربر",
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name="ساختمان",
    )

    role = models.ForeignKey(
        BuildingRole,
        on_delete=models.PROTECT,
        related_name="memberships",
        verbose_name="نقش",
    )

    def __str__(self):
        return f"{self.user} - {self.building} - {self.role}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "building", "role"],
                name="unique_user_building_role",
            )
        ]

        verbose_name = "عضویت ساختمان"
        verbose_name_plural = "عضویت‌های ساختمان"


class Unit(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="units",
        verbose_name="ساختمان",
    )

    number = models.PositiveIntegerField(
        verbose_name="شماره واحد",
    )

    code = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="کد واحد",
    )

    def __str__(self):
        return f"{self.building} - واحد {self.number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["building", "number"],
                name="unique_number_per_building",
            )
        ]

        verbose_name = "واحد"
        verbose_name_plural = "واحدها"


class BuildingExpense(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name="ساختمان",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان هزینه",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ (تومان)",
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت",
    )

    @property
    def jalali_date(self):
        local_date = timezone.localtime(self.created_at).date()

        return jdatetime.date.fromgregorian(
            date=local_date,
        ).strftime("%Y/%m/%d")

    def __str__(self):
        return f"{self.title} - {self.amount:,} تومان"

    class Meta:
        verbose_name = "هزینه ساختمان"
        verbose_name_plural = "هزینه‌های ساختمان"
