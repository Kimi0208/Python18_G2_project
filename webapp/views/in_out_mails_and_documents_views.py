from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from webapp.forms import CompaniesListForm, InOutMailsForm
from webapp.models import InOutMails, CompaniesList, ContractRegistry
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from docxtpl import DocxTemplate
from shutil import copyfile
from webapp.views.mail_send import send_email_notification
from django.db.models import ForeignKey
import json


class CompanyCreateView(CreateView):
    model = CompaniesList
    form_class = CompaniesListForm
    template_name = 'company_create.html'

    def form_valid(self, form):
        company = form.save(commit=False)
        company.save()
        return redirect(reverse_lazy('webapp:companies_list_view'))


class CompaniesListView(ListView):
    model = CompaniesList
    context_object_name = 'companies'
    template_name = 'companies_list.html'



class InOutMailsCreateView(CreateView):
    model = InOutMails
    form_class = InOutMailsForm
    template_name = ''