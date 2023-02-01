from django.urls import path, include
from rest_framework import routers
from vote.views import LoginView, VotingView


router = routers.DefaultRouter()
router.register('voting', VotingView, basename='voting')

urlpatterns = [
    path('login/', LoginView.as_view()),
]

urlpatterns += router.urls