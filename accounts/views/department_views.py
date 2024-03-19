from django.db.models import Count
from django.shortcuts import redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from accounts.forms import MyUserCreationForm, UserChangeForm, MyPasswordChangeForm, UserForm, DepartmentForm
from accounts.models import DefUser, Position, Department


class DepartmentListView(ListView):
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        queryset = Department.objects.annotate(num_users=Count('position__defuser'))
        return queryset


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_add.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:department_list')


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_update.html'

    def get_success_url(self):
        return reverse('accounts:department_list')


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'departments/department_delete.html'

    def get_success_url(self):
        return reverse('accounts:department_list')