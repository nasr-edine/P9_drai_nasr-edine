# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Ticket
# Create your views here.


class TicketListView(ListView):
    model = Ticket
    template_name = "home.html"


class TicketDetailView(DetailView):
    model = Ticket
    template_name = "ticket_detail.html"


class TicketCreateView(CreateView):
    model = Ticket
    template_name = "ticket_new.html"
    fields = '__all__'


class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = "ticket_edit.html"
    fields = ['title', 'body', 'image']
    # fields = '__all__'


class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = "ticket_delete.html"
    success_url = reverse_lazy('home')
