from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.forms import CommentForm
from webapp.models import Comment, Task
from webapp.views.task_views import get_user_info


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_proporsal_create.html'

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


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_proporsal_edit.html'

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


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'partial/comment_delete.html'

    def form_valid(self, form):
        comment_id = self.object.id
        self.object.delete()
        return JsonResponse({'comment_id': comment_id})
