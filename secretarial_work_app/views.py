from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from secretarial_work_app.forms import CompaniesListForm, ContractsForm, InMailsForm, OutMailsForm
from secretarial_work_app.models import CompaniesList, ContractRegistry, InMails, OutMails
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class CompanyCreateView(CreateView):
    model = CompaniesList
    form_class = CompaniesListForm
    template_name = 'company_create.html'

    def form_valid(self, form):
        company = form.save(commit=False)
        if 'attachment' in self.request.FILES:
            company.contract_with_company = self.request.FILES['attachment']
        company.save()
        return redirect(reverse_lazy('secretary:companies_list_view'))


class CompanyListView(ListView):
    model = CompaniesList
    context_object_name = 'companies'
    template_name = 'companies_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = CompaniesList.objects.all()
        return context


class CompanyUpdateView(UpdateView):
    model = CompaniesList
    form_class = CompaniesListForm
    template_name = 'company_update.html'
    success_url = reverse_lazy('secretary:companies_list_view')

    def form_valid(self, form):
        company = form.save(commit=False)
        if 'attachment' in self.request.FILES:
            company.contract_with_company = self.request.FILES['attachment']
            company.save()
            return redirect(reverse_lazy('secretary:companies_list_view'))


class CompanyDeleteView(DeleteView):
    model = CompaniesList
    template_name = 'company_delete.html'
    success_url = reverse_lazy('secretary:companies_list_view')


class ContractsCreateView(CreateView):
    model = ContractRegistry
    form_class = ContractsForm
    template_name = 'contracts_create.html'
    success_url = reverse_lazy('secretary:contracts_list_view')

    # def form_valid(self, form):
    #     contract = form.save(commit=False)
    #     if 'attachment' in self.request.FILES:
    #         contract.attachment = self.request.FILES['attachment']
    #     contract.save()
    #     return redirect(reverse_lazy('secretary:contracts_list_view'))


class ContractsListView(ListView):
    model = ContractRegistry
    context_object_name = 'contracts'
    template_name = 'contracts_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContractsUpdateView(UpdateView):
    model = ContractRegistry
    context_object_name = 'contracts'
    form_class = ContractsForm


    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     if 'attachment' in self.request.FILES:
    #         self.object.attachment = self.request.FILES['attachment']
    #         self.object.save()
    #         return redirect(reverse_lazy('secretary:contracts_list_view'))


class ContractDeleteView(DeleteView):
    model = ContractRegistry
    template_name = ''
    success_url = reverse_lazy('secretary:contracts_list_view')


class InMailsListView(ListView):
    model = InMails
    context_object_name = 'in_mails'
    template_name = 'in_mails_list.html'


class OutMailsListView(ListView):
    model = OutMails
    context_object_name = 'out_mails'
    template_name = 'out_mails_list.html'


class InMailsCreateView(CreateView):
    model = InMails
    form_class = InMailsForm
    template_name = 'in_mails_create.html'
    success_url = reverse_lazy('secretary:in_mails_list_view')

    # def form_valid(self, form):
    #     in_mails = form.save(commit=False)
    #     if 'attachment' in self.request.FILES:
    #         in_mails.attachment = self.request.FILES['attachment']
    #     in_mails.save()
    #     return redirect(reverse_lazy('secretary:in_mails_list_view'))


class OutMailsCreateView(CreateView):
    model = OutMails
    form_class = OutMailsForm
    template_name = 'out_mails_create.html'
    success_url = reverse_lazy('secretary:out_mails_list_view')

    # def form_valid(self, form):
    #     out_mails = form.save(commit=False)
    #     if 'attachment' in self.request.FILES:
    #         out_mails.attachment = self.request.FILES['attachment']
    #     out_mails.save()
    #     return redirect(reverse_lazy('secretary:out_mails_list_view'))
