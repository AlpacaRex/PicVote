from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from vote.models import Voting, User
from vote.serializers import VotingSerializer, VotingListSerializer


class UserView(APIView):
    def get(self, request):
        openid = request.headers.get('x-wx-openid')
        user = User.objects.get(openid=openid)
        votings = Voting.objects.filter(user=user)
        return Response(VotingListSerializer(instance=votings, many=True).data)


class VotingView(RetrieveModelMixin, GenericViewSet):

    queryset = Voting.objects.all()
    serializer_class = VotingSerializer

    def create(self, request):
        openid = request.headers.get('x-wx-openid')
        if not User.objects.filter(pk=openid):
            User.objects.create(pk=openid)
        data = request.data
        data['user'] = openid
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)






