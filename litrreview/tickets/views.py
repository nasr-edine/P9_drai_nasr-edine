from django.db.models import fields
from django.http import request
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm, ResponseForm  # new
from django import forms
from django.shortcuts import render, get_object_or_404
from django.forms import ModelForm

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


# class TicketForm(forms.Form):
#     title = forms.CharField(max_length=128)
#     description = forms.TextField(max_length=2048)
#     # time_created = forms.DateTimeField(auto_now_add=True)
#     image = forms.ImageField(upload_to='images/', null=True, blank=True)


# class ReviewForm(ModelForm):
#     class Meta:
#         model = Review
#         fields = ['headline', 'rating', 'body']


# def MyView(request):
#     if request.method == 'POST':
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             pass  # does nothing, just trigger the validation
#     else:
#         form = TicketForm()
#     return render(request, 'home.html', {'form': form})


# class MyView(LoginRequiredMixin, TemplateView):
#     form_class = TicketForm
#     # form_class2 = ReviewForm
#     if form_class.is_valid():
#         school = form_class.save(commit=False)
#         school.save()

#     def get(self, request):
#         return render(request, 'name.html', {
#             'form': self.form_class,
#             # "form2": self.form_class2
#         })


# class QuestionDetail(LoginRequiredMixin, View):
#     template_name = 'review_ticket_new.html'

#     def get_context_data(self, **kwargs):
#         # kwargs['question'] = self.get_object()
#         # if 'response_form' not in kwargs:
#         kwargs['response_form'] = ResponseForm()
#         # if 'comment_form' not in kwargs:
#         kwargs['comment_form'] = CommentForm()

#         return kwargs


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


