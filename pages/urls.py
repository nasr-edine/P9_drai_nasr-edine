from django.urls import path
from .views import homePageView, aboutPage

urlpatterns = [
    path('about/', aboutPage.as_view(), name='about'),
    path('', homePageView.as_view(), name='home'),
]
