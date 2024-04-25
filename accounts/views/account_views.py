from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.forms import MyUserCreationForm, UserChangeForm, MyPasswordChangeForm, UserForm
from django.contrib.auth.views import PasswordChangeView
from accounts.models import DefUser, Department
from accounts.models import DefUser, Position, Department


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = DefUser
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Данные пользователя успешно обновлены.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class UserPasswordChangeView(UserPassesTestMixin, PasswordChangeView):
    template_name = 'user_password_change.html'
    form_class = MyPasswordChangeForm

    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_obj'] = get_object_or_404(DefUser, pk=self.kwargs.get('pk'))
        return context


class UserListView(ListView):
    model = DefUser
    template_name = 'user_crud/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = DefUser
    form_class = UserForm
    template_name = 'user_crud/user_add.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data.get('password'))
        self.object.save()
        return redirect('accounts:user_list')


class UserUpdateView(UpdateView):
    model = DefUser
    form_class = UserForm
    template_name = 'user_crud/user_update.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data.get('password'))
        self.object.save()
        return redirect('accounts:user_list')


def user_delete(request, pk):
    user = get_object_or_404(DefUser, pk=pk)
    user.delete()

    return redirect(reverse_lazy('accounts:user_list'))
