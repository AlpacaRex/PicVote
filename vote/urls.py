from django.urls import path

from vote.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view())
]