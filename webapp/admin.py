from django.contrib import admin
from webapp.models import Task, Proposal, Priority, Comment, Status


admin.site.register(Task)
admin.site.register(Proposal)
admin.site.register(Priority)
admin.site.register(Comment)
admin.site.register(Status)