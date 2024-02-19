from django.contrib import admin
from accounts.models import Department, Position, DefUser


admin.site.register(Department)
admin.site.register(Position)
admin.site.register(DefUser)