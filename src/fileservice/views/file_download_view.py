import os
from typing import Any

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.authentication import login_required
from src.accounts.models import User
from src.basecore.custom_error_handler import BadRequestError, NotFoundError
from src.basecore.responses import OkResponse
from src.fileservice.models import File
from src.fileservice.serializers.file_serializer import FileSerializer


class FileDownloadView(generics.GenericAPIView):

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> Response:

        serializer = FileSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        file_id = serializer.validated_data.get('id')

        queryset = File.objects.get(id=file_id)
        if not queryset.user.id == user.id:
            raise BadRequestError(f'This user doesn`t have this file in own repistory')

        file_path = queryset.destination

        if not os.path.exists(file_path):
            raise NotFoundError('file doesn`t exist in storrage')

        return Response(headers={'Content-Disposition': f'attachment; filename="{file_path}"'})
