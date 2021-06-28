from itertools import chain

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.models import UserFollows

from .forms import TicketReviewForm
from .models import Review, Ticket


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "ticket_list.html"
    login_url = 'login'

    def get_queryset(self):
        # ordered_tickets_by_date = self.model.objects.order_by('-time_created')
        # ordered_review_by_date = Review.objects.order_by('-time_created')
        # todo add filter for users I follow
        # Get instances of my following
        my_following = UserFollows.objects.filter(user=self.request.user)

        # Get id list of my following
        following_ticket_list = [
            follower.followed_user.id for follower in my_following]

        # include also myself in list for display my own posts
        following_ticket_list.append(self.request.user.id)

        # Finally filter all posts by my following list
        filtered_tickets_by_users_i_follow = self.model.objects.filter(
            user__in=following_ticket_list)
        filtered_reviews_by_users_i_follow = Review.objects.filter(
            user__in=following_ticket_list)

        #  the merge/combine operator | only works on querysets from the same model and before the slicing it.
        # mergeQueryset = filtered_tickets_by_users_i_follow | filtered_reviews_by_users_i_follow  # merge querysets
        # recent_stories = mergeQueryset.distinct().order_by('-date')

        ticket_and_review_merged = sorted(chain(
            filtered_tickets_by_users_i_follow, filtered_reviews_by_users_i_follow),
            key=lambda instance: instance.time_created, reverse=True)

        return ticket_and_review_merged


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "ticket_detail.html"
    login_url = 'login'


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ('title', 'description', 'image',)
    template_name = "ticket_edit.html"
    success_url = reverse_lazy('ticket_current_user_list')
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
    success_url = reverse_lazy('ticket_list')

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


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_edit.html"
    success_url = reverse_lazy('ticket_current_user_list')
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
