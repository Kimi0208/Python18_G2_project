from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from secretarial_work_app.forms import CompaniesListForm, ContractsForm, InMailsForm, OutMailsForm
from secretarial_work_app.models import CompaniesList, ContractRegistry, InMails, OutMails, Attachment
from django.views.generic import ListView, CreateView, UpdateView


class CompanyCreateView(CreateView):
    model = CompaniesList
    form_class = CompaniesListForm
    template_name = 'company_create.html'
    success_url = reverse_lazy('secretary:companies_list_view')


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


def company_delete(request, pk):
    company = get_object_or_404(CompaniesList, pk=pk)
    company.delete()
    return redirect(reverse_lazy('secretary:companies_list_view'))


class ContractsCreateView(CreateView):
    model = ContractRegistry
    form_class = ContractsForm
    template_name = 'contracts_create.html'
    success_url = reverse_lazy('secretary:contracts_list_view')

    def form_valid(self, form):
        contract = form.save()
        contract.document_auto_number = contract.pk
        contract.save()

        files = form.cleaned_data['attachment']
        for file in files:
            attachment = Attachment.objects.create(file=file)
            contract.attachments.add(attachment)

        return redirect(reverse_lazy('secretary:contracts_list_view'))


class ContractsListView(ListView):
    model = ContractRegistry
    context_object_name = 'contracts'
    template_name = 'contracts_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attachments'] = Attachment.objects.all()
        return context


class ContractsUpdateView(UpdateView):
    model = ContractRegistry
    context_object_name = 'contracts'
    template_name = 'contracts_update.html'
    form_class = ContractsForm
    success_url = reverse_lazy('secretary:contracts_list_view')

    def form_valid(self, form):
        contract = form.save()
        contract.document_auto_number = contract.id
        contract.save()

        files = form.cleaned_data['attachment']
        for file in files:
            attachment = Attachment.objects.create(file=file)
            contract.attachments.add(attachment)

        return redirect(reverse_lazy('secretary:contracts_list_view'))


def attachment_delete(request, contract_id, attachment_id):
    attachment = get_object_or_404(Attachment, pk=attachment_id)
    attachment.delete()
    return redirect("secretary:contracts_update_view", pk=contract_id)


def contract_delete(request, pk):
    contract = get_object_or_404(ContractRegistry, pk=pk)
    if contract.attachments:
        for attachment in contract.attachments.all():
            Attachment.objects.filter(id=attachment.id).delete()
    contract.delete()

    return redirect(reverse_lazy('secretary:contracts_list_view'))


class InMailsListView(ListView):
    model = InMails
    context_object_name = 'in_mails'
    template_name = 'in_mails_list.html'


class InMailsCreateView(CreateView):
    model = InMails
    form_class = InMailsForm
    template_name = 'in_mails_create.html'
    success_url = reverse_lazy('secretary:in_mails_list_view')


class InMailsUpdateView(UpdateView):
    model = InMails
    form_class = InMailsForm
    template_name = 'in_mails_update.html'
    success_url = reverse_lazy('secretary:in_mails_list_view')


def in_mail_delete(request, pk):
    in_mails = get_object_or_404(InMails, pk=pk)
    in_mails.delete()
    return redirect(reverse_lazy('secretary:in_mails_list_view'))


class OutMailsListView(ListView):
    model = OutMails
    context_object_name = 'out_mails'
    template_name = 'out_mails_list.html'


class OutMailsCreateView(CreateView):
    model = OutMails
    form_class = OutMailsForm
    template_name = 'out_mails_create.html'
    success_url = reverse_lazy('secretary:out_mails_list_view')


class OutMailsUpdateView(UpdateView):
    model = OutMails
    form_class = OutMailsForm
    template_name = 'out_mails_update.html'
    success_url = reverse_lazy('secretary:out_mails_list_view')


def out_mail_delete(request, pk):
    out_mail = get_object_or_404(OutMails, pk=pk)
    out_mail.delete()
    return redirect(reverse_lazy('secretary:out_mails_list_view'))
