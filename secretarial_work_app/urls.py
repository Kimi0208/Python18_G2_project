from django.urls import path
from secretarial_work_app.views import (CompanyCreateView, CompanyListView, ContractsListView, ContractsCreateView,
                                        InMailsListView, OutMailsListView, InMailsCreateView, OutMailsCreateView,
                                        contract_delete, ContractsUpdateView, company_delete, CompanyUpdateView,
                                        in_mail_delete, InMailsUpdateView, OutMailsUpdateView, out_mail_delete)

app_name = 'secretary'

urlpatterns = [

    path('companies/', CompanyListView.as_view(), name='companies_list_view'),
    path('companies/create/', CompanyCreateView.as_view(), name='company_create_view'),
    path('companies/<int:pk>/update', CompanyUpdateView.as_view(), name='company_update_view'),
    path('companies/<int:pk>/delete', company_delete, name='company_delete_view'),
    path('contracts/', ContractsListView.as_view(), name='contracts_list_view'),
    path('contracts/create/', ContractsCreateView.as_view(), name='contracts_create_view'),
    path('contracts/<int:pk>/update', ContractsUpdateView.as_view(), name='contracts_update_view'),
    path('contracts/<int:pk>/delete', contract_delete, name='contracts_delete_view'),
    path('inmails/', InMailsListView.as_view(), name='in_mails_list_view'),
    path('inmails/create/', InMailsCreateView.as_view(), name='in_mails_create_view'),
    path('inmails/<int:pk>/update', InMailsUpdateView.as_view(), name='in_mails_update_view'),
    path('inmails/<int:pk>/delete', in_mail_delete, name='in_mails_delete_view'),
    path('outmails/', OutMailsListView.as_view(), name='out_mails_list_view'),
    path('outmails/create/', OutMailsCreateView.as_view(), name='out_mails_create_view'),
    path('outmails/<int:pk>/update', OutMailsUpdateView.as_view(), name='out_mails_update_view'),
    path('outmails/<int:pk>/delete', out_mail_delete, name='out_mails_delete_view'),
]
