from django import forms
from secretarial_work_app.models import CompaniesList, ContractRegistry, InMails, OutMails


class CompaniesListForm(forms.ModelForm):

    class Meta:
        model = CompaniesList
        fields = ['company_code', 'company_name', 'company_inn', 'contract_location', 'attachment']


class ContractsForm(forms.ModelForm):

    class Meta:
        model = ContractRegistry
        fields = ['company', 'input_contract_number', 'description', 'consultion_date', 'responsible_employee',
                  'scan_copy', 'attachment', 'contract_location', 'attachment']
        widgets = {
            'consultion_date' : forms.DateInput(attrs={'type': 'date'})
        }


class InMailsForm(forms.ModelForm):

    class Meta:
        model = InMails
        fields = ['in_mail_number', 'mail_number', 'sender', 'description', 'pages_count', 'responsible_person',
                  'output_mail_number', 'status', 'scan', 'attachment', 'comments']


class OutMailsForm(forms.ModelForm):

    class Meta:
        model = OutMails
        fields = ['out_mail_number', 'receiver', 'description', 'pages_count', 'input_mail_number',
                  'responsible_person', 'status', 'scan', 'attachment', 'comments']
