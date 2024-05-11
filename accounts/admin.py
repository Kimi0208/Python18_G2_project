from django.contrib import admin
from accounts.models import Department, Position, DefUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(Department)
admin.site.register(Position)


class CustomUserAdmin(UserAdmin):
    model = DefUser
    list_display = ('username', 'first_name', 'email', 'phone_number')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ('first_name', 'last_name', 'patronymic', 'email', 'email_password',
                                        'phone_number', 'position', 'signature')}),
        (
            ("Permissions"),
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
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('username', 'first_name', 'last_name', 'patronymic', 'password1', 'password2', 'email',
                           'email_password', 'phone_number', 'position', 'signature'),
            },
        ),
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")


admin.site.register(DefUser, CustomUserAdmin)