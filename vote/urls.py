from django.urls import path, include
from rest_framework import routers
from vote.views import UserView, VotingView, VotingItemView, QRCodeView, DeleteVotingView

router = routers.DefaultRouter()
router.register('voting', VotingView, basename='voting')
router.register('votingItem', VotingItemView, basename='votingItem')

urlpatterns = [
    path('user/', UserView.as_view()),
    path('qrcode/', QRCodeView.as_view()),
    path('deleteVoting/', DeleteVotingView.as_view()),
]

urlpatterns += router.urls