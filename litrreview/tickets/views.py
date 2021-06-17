from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Ticket
from .models import Review


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "ticket_list.html"
    login_url = 'login'

    def get_queryset(self):
        ordered_tickets_by_date = self.model.objects.order_by('-time_created')
        return ordered_tickets_by_date


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "ticket_detail.html"
    login_url = 'login'


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ('title', 'description', 'image',)
    template_name = "ticket_edit.html"
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "ticket_delete.html"
    success_url = reverse_lazy('ticket_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = "ticket_new.html"
    fields = ('title', 'description', 'image')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketCurrentUserView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket_current_user_list.html'
    login_url = 'login'

    def get_queryset(self):
        posts_current_user = self.model.objects.filter(user=self.request.user)
        ordered_posts_current_user = posts_current_user.order_by(
            '-time_created')
        return ordered_posts_current_user


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = "review_new.html"
    fields = ('headline', 'rating', 'body')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        ctx = self.get_context_data()

        form.instance.ticket = ctx['ticket']
        return super().form_valid(form)


# class ResponseForm(forms.Form):
#     content = forms.CharField()


# class CommentForm(forms.Form):
#     content = forms.CharField()


# class ReviewAndTicketCreateView(CreateView):
#     model = ReviewAndTicket
#     template_name = "reviewandticket_new.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['ticket'] = Ticket.objects.get(pk=self.kwargs['pk'])
    #     context['form_ticket'] =
    #     return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ('headline', 'rating', 'body',)
    template_name = "review_edit.html"
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "review_delete.html"
    success_url = reverse_lazy('ticket_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
