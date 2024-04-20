from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from accounts.views.views import UserCreateView, UserUpdateView, UserDeleteView

from accounts.views.views import UserDetailView, UserChangeView, UserPasswordChangeView, UserListView
from accounts.views.department_views import DepartmentListView, DepartmentCreateView, DepartmentUpdateView, \
    DepartmentDeleteView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/change/', UserChangeView.as_view(), name='user_change'),
    path('<int:pk>/password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='add_user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('group_list/', DepartmentListView.as_view(), name='department_list'),
    path('create/department', DepartmentCreateView.as_view(), name='create_department'),
    path('<int:pk>/update_department/', DepartmentUpdateView.as_view(), name='update_department'),
    path('<int:pk>/delete_department/', DepartmentDeleteView.as_view(), name='delete_department'),
]
