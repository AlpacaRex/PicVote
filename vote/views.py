from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from vote.models import Voting, User
from vote.serializers import VotingSerializer


class LoginView(APIView):
    def post(self, request):
        code = request.data.get('code')

        return Response({'msg': 'nmsl'})


class VotingView(GenericViewSet):

    queryset = Voting.objects.all()
    serializer_class = VotingSerializer

    def create(self, request):
        openid = request.headers.get('openid')
        print(openid)
        if not User.objects.filter(pk=openid):
            User.objects.create(pk=openid)
        data = request.data.dict()
        data['user'] = openid
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)






