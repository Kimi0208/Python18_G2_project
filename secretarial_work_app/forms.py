from django import forms
from secretarial_work_app.models import CompaniesList, ContractRegistry, InMails, OutMails


class CompaniesListForm(forms.ModelForm):

    class Meta:
        model = CompaniesList
        fields = ['company_code', 'company_name', 'company_inn', 'contract_location', 'attachment']


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class ContractsForm(forms.ModelForm):
    attachment = MultipleFileField(required=False)

    class Meta:
        model = ContractRegistry
        fields = ['company', 'input_contract_number', 'description', 'consultion_date', 'responsible_employee',
                  'scan_copy', 'attachment', 'contract_location']
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
