from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from vote.models import Voting, User, VotingItem
from vote.serializers import VotingSerializer, VotingListSerializer


class UserView(APIView):
    def get(self, request):
        openid = request.headers.get('x-wx-openid')
        if not User.objects.filter(openid=openid).exists():
            return Response([])
        user = User.objects.get(openid=openid)
        votings = Voting.objects.filter(user=user)
        if votings.exists():
            return Response(VotingListSerializer(instance=votings, many=True).data)
        else:
            return Response([])


class VotingView(RetrieveModelMixin, GenericViewSet):

    queryset = Voting.objects.all()
    serializer_class = VotingSerializer

    def create(self, request):
        openid = request.headers.get('x-wx-openid')
        if not User.objects.filter(pk=openid).exists():
            User.objects.create(pk=openid)
        data = request.data
        data['user'] = openid
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            voting = serializer.save()
            for index, item in enumerate(data['file_list']):
                VotingItem.objects.create(fileID=item['fileID'], voting=voting, order=index+1)
        return Response(serializer.data)

    def list(self, request):
        return Response({'num': len(self.get_queryset())})
