from django.urls import path

from .views import TicketListView, TicketUpdateView, TicketDetailView, TicketDeleteView, TicketCreateView, TicketCurrentUserView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket_edit'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket_delete'),
    path('', TicketListView.as_view(), name='ticket_list'),
    path('new/', TicketCreateView.as_view(), name='ticket_new'),
    path('list/', TicketCurrentUserView.as_view(),
         name='ticket_current_user_list'),
    path('<int:pk>/newcomment/', ReviewCreateView.as_view(), name='review_new'),
    path('<int:pk>/editreview/', ReviewUpdateView.as_view(), name='review_edit'),
    path('<int:pk>/deletereview/', ReviewDeleteView.as_view(), name='review_delete'),
]
