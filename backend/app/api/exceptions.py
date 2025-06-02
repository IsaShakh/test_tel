from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "type": "error",
            "errors": response.data
        }
    else:
        response = Response({
            "type": "error",
            "errors": "Внутренняя ошибка сервера"
        }, status=500)

    return response