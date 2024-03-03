from django.contrib import admin

from webapp.models import Task, Proposal, Comment, Status, Priority, File

admin.site.register(Task)
admin.site.register(Proposal)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(File)
