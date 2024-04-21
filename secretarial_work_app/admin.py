from django.contrib import admin
from secretarial_work_app.models import (InMails, InOutMailsStatus, OutMails, CompaniesList, ContractRegistry,
                                         ContractLocation)

admin.site.register(InMails)
admin.site.register(InOutMailsStatus)
admin.site.register(OutMails)
admin.site.register(CompaniesList)
admin.site.register(ContractRegistry)
admin.site.register(ContractLocation)