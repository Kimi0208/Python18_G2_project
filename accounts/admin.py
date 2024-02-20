from django.contrib import admin

from accounts.models import CustomUser, Position, Department

admin.site.register(CustomUser)
admin.site.register(Position)
admin.site.register(Department)
