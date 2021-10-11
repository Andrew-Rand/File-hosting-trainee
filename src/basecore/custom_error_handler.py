from rest_framework import status, exceptions, serializers
from rest_framework.response import Response

from src.basecore.std_response import create_std_response


class BadRequestError(Exception):
    def __init__(self, *args):
        super().__init__(args)


def error_handler(exc: Exception, context) -> Response:

    if isinstance(exc, BadRequestError):
        return Response(create_std_response(status_code=status.HTTP_400_BAD_REQUEST, info=exc.args))

    elif isinstance(exc, exceptions.AuthenticationFailed):
        return Response(create_std_response(status_code=status.HTTP_401_UNAUTHORIZED, info=exc.args))

    elif isinstance(exc, serializers.ValidationError):
        return Response(create_std_response(status_code=status.HTTP_400_BAD_REQUEST, info=exc.args))

    elif isinstance(exc, ValueError):
        return Response(create_std_response(status_code=status.HTTP_400_BAD_REQUEST, info=exc.args))
