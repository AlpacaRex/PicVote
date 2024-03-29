from datetime import datetime

from django.db.models import F
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from vote.models import Voting, User, VotingItem
from vote.serializers import VotingSerializer, VotingListSerializer, VotingItemSerializer
import requests
import base64


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


class VoteView(GenericViewSet):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.deadline < datetime.now():
            return Response({'errmsg': '投票已截止'})
        elif instance.history.filter(pk=request.headers.get('x-wx-openid')).exists():
            return Response({'errmsg': '已参与过投票'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class VotingDetailView(RetrieveModelMixin , GenericViewSet):
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
        else:
            print(serializer.errors)
        return Response(serializer.data)

    def list(self, request):
        return Response({'num': len(self.get_queryset())})

    def delete(self, request):
        for voting_id in request.data.get('voting_id_list'):
            self.get_queryset().get(pk=voting_id).delete()
        votings = Voting.objects.filter(user_id=request.headers.get('x-wx-openid'))
        if votings.exists():
            return Response(VotingListSerializer(instance=votings, many=True).data)
        else:
            return Response([])


class VotingItemView(GenericViewSet):
    serializer_class = VotingItemSerializer

    def create(self, request):
        voting = Voting.objects.get(pk=request.data['voting_id'])
        for index, item in enumerate(request.data['file_list']):
            VotingItem.objects.create(
                fileID=item['fileID'],
                voting=voting,
                order=index + 1,
                title=item['title'],
                description=item['description']
            )
        return Response({'msg': 'successfully created'})

    def list_update(self, request):
        voting_items = VotingItem.objects.filter(voting_id=request.data.get('voting_id'))
        voting_items.filter(order__in=request.data.get('first_prize')).update(first_prize=F('first_prize')+1)
        voting_items.filter(order__in=request.data.get('second_prize')).update(second_prize=F('second_prize')+1)
        voting_items.filter(order__in=request.data.get('third_prize')).update(second_prize=F('third_prize')+1)
        user, b = User.objects.get_or_create(pk=request.headers.get('x-wx-openid'))
        voting_items[0].voting.history.add(user)
        return Response({'msg': 'successfully updated'})


class QRCodeView(APIView):

    def post(self, request):
        response = requests.post(
            url='http://api.weixin.qq.com/wxa/getwxacodeunlimit',
            json={
                'page': 'pages/vote/vote',
                'scene': str(request.data.get('id')),
                'check_path': False,
            }
        )
        return HttpResponse(base64.b64encode(response.content))


class DeleteVotingView(APIView):

    def post(self, request):
        voting_items = VotingItem.objects.filter(voting_id__in=request.data.get('voting_id'))
        return Response(VotingItemSerializer(instance=voting_items, many=True).data)

    def delete(self, request):
        Voting.objects.filter(id__in=request.data.get('voting_id')).delete()
        votings = Voting.objects.filter(user_id=request.headers.get('x-wx-openid'))
        if votings.exists():
            return Response(VotingListSerializer(instance=votings, many=True).data)
        else:
            return Response([])

