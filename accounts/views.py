from django.shortcuts import render
from accounts.models import Department, Position
from django.views.generic import ListView


class DepartamentListView(ListView):
    model = Department
    template_name = 'base.html'
    context_object_name = 'departments'


class PositionListView(ListView):
    model = Position
    template_name = 'base.html'
    context_object_name = 'positions'
