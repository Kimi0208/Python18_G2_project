from django.contrib import admin
from webapp.models import Task, Priority, Comment, Status, Type, Checklist


admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Checklist)