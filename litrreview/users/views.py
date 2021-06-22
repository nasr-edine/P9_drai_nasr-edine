from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView
from .forms import CustomUserCreationForm, FollowerForm
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .models import CustomUser, UserFollows

# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# class FollowUserView(LoginRequiredMixin, ListView):
#     model = UserFollows
#     template_name = 'follow_user_list.html'
#     login_url = 'login'

#     def get_queryset(self):
#         follow_user = self.model.objects.filter(user=self.request.user)
#         # ordered_posts_current_user = posts_current_user.order_by(
#         #     '-time_created')
#         followed_by = self.model.objects.filter(
#             followed_user=self.request.user)
#         return followed_by
#         # return follow_user

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['follow_user'] = self.model.objects.filter(
#             user=self.request.user)
#         context['followed_by'] = self.model.objects.filter(
#             followed_user=self.request.user)
#         return context


class FollowCreateView(LoginRequiredMixin, FormView):
    model = UserFollows
    login_url = 'login'
    context = {}
    form_class = FollowerForm
    template_name = "follow_user_list.html"

    success_url = reverse_lazy('follow')

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context['username'] = CustomUser.objects.all()
        # print(self.context['username'])

        self.context['follow_user'] = self.model.objects.filter(
            user=self.request.user)
        # print(self.request.user)
        self.context['followed_by'] = self.model.objects.filter(
            followed_user=self.request.user)
        return self.context

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        value = form.cleaned_data['follower']
        if value == self.request.user.username:
            print("You don't can subscrite to yourself")
            form.add_error(None, "You don't can subscribe to yourself")
            return self.form_invalid(form)
        try:
            user1 = CustomUser.objects.get(username=value)
        except CustomUser.DoesNotExist:
            form.add_error(None, "This user don't exist,")
            return self.form_invalid(form)
        test2 = self.model.objects.filter(
            Q(followed_user=user1.id) & Q(user=self.request.user)
        )
        if test2:
            form.add_error(None, "You are already subscribed at this user,")
            return self.form_invalid(form)
        else:
            print("OK")
            test3 = UserFollows.objects.create(
                user=self.request.user, followed_user=user1)
            print(test3)
        return super().form_valid(form)


class FollowDeleteView(LoginRequiredMixin, DeleteView):
    model = UserFollows
    template_name = "follow_delete.html"
    success_url = reverse_lazy('follow')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
