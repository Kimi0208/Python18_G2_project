from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.forms import CommentForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from webapp.models import Comment, Task


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
        comment = {
            'description': self.object.description,
            'id': self.object.id,
            'author_first_name': self.object.author.first_name,
            'author_last_name': self.object.author.last_name,
            'task': self.object.task.id,
            'created_at': self.object.created_at,
            'updated_at': self.object.updated_at,
            'author_id': self.object.author.id,
            'user_id': self.request.user.id
        }
        return JsonResponse({'comment': comment})


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_proporsal_edit.html'
    permission_required = 'webapp.change_comment'

    def form_valid(self, form):
        self.object = form.save()
        comment = {
            'description': self.object.description,
            'id': self.object.id,
            'author_first_name': self.object.author.first_name,
            'author_last_name': self.object.author.last_name,
            'task': self.object.task.id,
            'created_at': self.object.created_at,
            'updated_at': self.object.updated_at,
            'author_id': self.object.author.id,
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
