from django.http import JsonResponse
from django.views.generic import CreateView
from webapp.forms import CommentForm
from webapp.models import Comment, Task


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_proporsal_create.html'

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
            'updated_at': self.object.updated_at
        }
        return JsonResponse({'comment': comment})
