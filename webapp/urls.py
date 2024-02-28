from django.urls import path

from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView,
                          ProposalListView, ProposalCreateView, ProposalUpdateView, ProposalDeleteView, index_view)

app_name = 'webapp'

urlpatterns = [
    # path('', index_view, name='index'),
    path('', TaskListView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('proposals/', ProposalListView.as_view(), name='proposals'),
    path('proposals/create/', ProposalCreateView.as_view(), name='proposal_create'),
    path('proposals/update/<int:pk>/', ProposalUpdateView.as_view(), name='proposal_update'),
    path('proposals/delete/<int:pk>', ProposalDeleteView.as_view(), name='proposal_delete'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail')
]