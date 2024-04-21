from django.urls import path
from secretarial_work_app.views import (CompanyCreateView, CompanyListView, ContractsListView, ContractsCreateView,
                          InMailsListView, OutMailsListView, InMailsCreateView, OutMailsCreateView)

app_name = 'secretary'

urlpatterns = [

    path('companies/', CompanyListView.as_view(), name='companies_list_view'),
    path('companies/create/', CompanyCreateView.as_view(), name='company_create_view'),
    path('contracts/', ContractsListView.as_view(), name='contracts_list_view'),
    path('contracts/create/', ContractsCreateView.as_view(), name='contracts_create_view'),
    path('inmails/', InMailsListView.as_view(), name='in_mails_list_view'),
    path('outmails/', OutMailsListView.as_view(), name='out_mails_list_view'),
    path('inmails/create/', InMailsCreateView.as_view(), name='in_mails_create_view'),
    path('outmails/create/', OutMailsCreateView.as_view(), name='out_mails_create_view'),
]
