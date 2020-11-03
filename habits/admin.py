from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from ordered_model.admin import OrderedModelAdmin

from habits import models


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "date_joined")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "timezone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("password1", "password2")},),
    )


@admin.register(models.Habit)
class HabitAdmin(OrderedModelAdmin):
    list_display = ('edit', 'name', 'days', 'morning', 'reminder_time', 'move_up_down_links', 'active')
    list_editable = ('name', 'days', 'morning', 'reminder_time', 'active')

    def edit(self, _):
        return 'edit'


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'completed', 'date')
    list_editable = ('completed',)
