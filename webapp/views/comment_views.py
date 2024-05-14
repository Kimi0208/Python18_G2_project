from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.forms import CommentForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from webapp.models import Comment, Task
from webapp.views.task_views import get_user_info


class CommentCreateView(PermissionRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_proporsal_create.html'
    permission_required = 'webapp.add_comment'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.task = Task.objects.get(pk=self.kwargs['task_pk'])
        self.object.save()
        author = get_user_info(self.request.user)
        comment = {
            'description': self.object.description,
            'id': self.object.id,
            'task': self.object.task.id,
            'created_at': self.object.created_at,
            'updated_at': self.object.updated_at,
            'author': author,
            'user_id': self.request.user.id
        }
        return JsonResponse({'comment': comment})


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_proporsal_edit.html'
    permission_required = 'webapp.change_comment'

    def has_permission(self):
        return super().has_permission() and self.request.user == self.get_object().author

    def form_valid(self, form):
        self.object = form.save()
        author = get_user_info(self.object.author)
        comment = {
            'description': self.object.description,
            'id': self.object.id,
            'author': author,
            'task': self.object.task.id,
            'created_at': self.object.created_at,
            'updated_at': self.object.updated_at,
            'user_id': self.request.user.id
        }
        return JsonResponse({'comment': comment})


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    template_name = 'partial/comment_delete.html'
    permission_required = 'webapp.delete_comment'

    def form_valid(self, form):
        comment_id = self.object.id
        self.object.delete()
        return JsonResponse({'comment_id': comment_id})
