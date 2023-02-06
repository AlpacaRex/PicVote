from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from vote.models import Voting, User, VotingItem
from vote.serializers import VotingSerializer, VotingListSerializer, VotingItemSerializer
import requests


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
            serializer.save()
        return Response(serializer.data)

    def list(self, request):
        return Response({'num': len(self.get_queryset())})

    def delete(self, request, pk):
        self.get_queryset().get(pk=pk).delete()
        return Response(self.get_serializer(self.get_queryset().filter(user=request.headers.get('x-wx-openid'))).data)


class VotingItemView(GenericViewSet):
    serializer_class = VotingItemSerializer

    def create(self, request):
        voting = Voting.objects.get(pk=request.data['voting_id'])
        for index, item in enumerate(request.data['file_list']):
            VotingItem.objects.create(fileID=item['fileID'], voting=voting, order=index + 1)
        return Response({'msg': 'successfully created'})

    def update(self, request, pk):
        voting_item = VotingItem.objects.get(pk=pk)
        voting_item.num += 1
        voting_item.save()
        return Response(self.get_serializer(instance=voting_item).data)


class QRCodeView(APIView):

    def post(self, request):
        response = requests.post(
            url='http://api.weixin.qq.com/wxa/getwxacodeunlimit',
            data={
                'page': 'pages/vote/vote',
                'scene': 'id=%d' % request.data.get('id'),
                'env_version': 'develop'
            }
        )
        return Response(response.json())
