from django.urls import path

from .views import FollowCreateView, FollowDeleteView, SignUpView

# from .views import SignUpView, FollowUserView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('follow', FollowUserView.as_view(), name='follow'),
    path('follow', FollowCreateView.as_view(), name='follow'),
    path('<int:pk>/delete/', FollowDeleteView.as_view(), name='follow_delete'),

]
