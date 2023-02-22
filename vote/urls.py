from django.urls import path, include
from rest_framework import routers
from vote.views import UserView, VotingDetailView, VotingItemView, QRCodeView, DeleteVotingView, VoteView

router = routers.DefaultRouter()
router.register('voting', VotingDetailView, basename='voting')
router.register('vote', VoteView, basename='vote')

urlpatterns = [
    path('user/', UserView.as_view()),
    path('qrcode/', QRCodeView.as_view()),
    path('deleteVoting/', DeleteVotingView.as_view()),
    path('votingItem/', VotingItemView.as_view({'post': 'create', 'put': 'list_update'}))
]

urlpatterns += router.urls