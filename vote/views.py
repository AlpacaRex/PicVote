from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    def post(self, request):
        code = request.data.get('code')

        return Response({'msg': 'nmsl'})

