from django.db.models import fields
from django.http import request
from django.views.generic import View, ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django import forms
from django.shortcuts import render, get_object_or_404
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from itertools import chain

from .models import Ticket
from .models import Review
from .forms import TicketReviewForm


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "ticket_list.html"
    login_url = 'login'

    def get_queryset(self):
        ordered_tickets_by_date = self.model.objects.order_by('-time_created')
        ordered_review_by_date = Review.objects.order_by('-time_created')
        result_list2 = sorted(chain(
            ordered_tickets_by_date, ordered_review_by_date), key=lambda instance: instance.time_created, reverse=True)
        return result_list2


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
        ordered_posts = posts_current_user.order_by('-time_created')
        reviews_current_user = Review.objects.filter(user=self.request.user)
        ordered_review = reviews_current_user.order_by('-time_created')
        result_list2 = sorted(chain(
            ordered_posts, ordered_review), key=lambda instance: instance.time_created, reverse=True)
        return result_list2


class ReviewForm(forms.ModelForm):
    CHOICES = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5')]
    rating = forms.ChoiceField(
        choices=CHOICES,
        label='rating',
    )
    body = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['headline'].label = "Titre"
        self.fields['rating'].label = "Note"
        self.fields['body'].label = "Commentaire"

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_new.html"
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


class TicketReviewCreateView(LoginRequiredMixin, FormView):
    model = Ticket
    login_url = 'login'
    # context = {}
    form_class = TicketReviewForm
    template_name = "review_ticket_new.html"

    success_url = reverse_lazy('ticket_list')

    def form_valid(self, form):

        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        image = form.cleaned_data['image']

        headline = form.cleaned_data['headline']
        body = form.cleaned_data['body']
        rating = form.cleaned_data['rating']

        ticket = Ticket(
            title=title,
            description=description,
            image=image,
            user=self.request.user,
        )
        ticket.save()
        review = Review(user=self.request.user, headline=headline,
                        rating=rating, body=body, ticket=ticket)
        review.save()
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
    form_class = ReviewForm
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
