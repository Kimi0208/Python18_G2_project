from django.urls import path
from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskView, add_subtasks,
                          delete_file, CompanyCreateView, CompaniesListView)

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/', TaskView.as_view(), name="task_proposal_view"),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('task/<int:task_pk>/<int:checklist_pk>', add_subtasks, name='add_subtasks'),
    # path('task/<int:task_pk>/file/', FileAddView.as_view(), name='add_file'),
    path('task/<int:task_pk>/file/<int:file_pk>/delete/', delete_file, name='delete_file'),
    path('companies/', CompaniesListView.as_view(), name='companies_list_view'),
    path('companies/create/', CompanyCreateView.as_view(), name='company_create_view'),
]
