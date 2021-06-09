from os import name
from django.urls import path

from .views import TicketListView, TicketDetailView, TicketCreateView, TicketUpdateView, TicketDeleteView

urlpatterns = [
    path('ticket/<int:pk>/delete', TicketDeleteView.as_view(), name='ticket_delete'),
    path('ticket/<int:pk>/edit', TicketUpdateView.as_view(), name='ticket_edit'),
    path('ticket/new', TicketCreateView.as_view(), name='ticket_new'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('', TicketListView.as_view(), name='home'),
]
