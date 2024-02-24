from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from webapp.forms import ProposalForm
from webapp.models import Proposal
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class ProposalListView(ListView):
    model = Proposal
    template_name = 'partial/proposal_list.html'
    context_object_name = 'proposals'


class ProposalCreateView(CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'task_proposal_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponse()


class ProposalUpdateView(UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'task_proposal_edit.html'

    def get_success_url(self):
        return reverse('webapp:index')


class ProposalDeleteView(DeleteView):
    model = Proposal
    template_name = 'task_proposal_delete.html'

    def get_success_url(self):
        return reverse('webapp:index')