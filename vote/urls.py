from django.urls import path, include
from rest_framework import routers
from vote.views import UserView, VotingView, VotingItemView

router = routers.DefaultRouter()
router.register('voting', VotingView, basename='voting')
router.register('votingItem', VotingItemView, basename='votingItem')

urlpatterns = [
    path('user/', UserView.as_view()),
]

urlpatterns += router.urls