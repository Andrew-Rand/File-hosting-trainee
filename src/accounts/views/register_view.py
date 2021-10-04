from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.serializers import UserSerializer


class RegisterView(generics.GenericAPIView):

    permission_classes = [AllowAny, ]

    def post(self, request: Request) -> Response:

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
