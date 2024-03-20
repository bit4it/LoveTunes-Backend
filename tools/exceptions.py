from rest_framework import status
from rest_framework.exceptions import APIException
from apps.core.models import CustomErrors
from apps.core.api.serializers import ErrorSerializer
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call the default exception handler first  
    response = exception_handler(exc, context)
    if response is not None:
        error_field = exc.__dict__.get("error")
        if error_field:
            print("Eror  field", error_field)
            if not exc.detail:
                response.data = exc.error
            else:
                response.data = exc.error
                response.data["detail"] = exc.detail

    return response


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = None
    default_code = None

    def __init__(self, detail=None, code=None, error_code=None):
        super().__init__(detail, code)
        try:
            self.detail = detail
            error = CustomErrors.objects.get(code=error_code)
            print(error)
            self.status_code = error.status_code
            serializer = ErrorSerializer(error)
            self.error = serializer.data
            print(self.error)
        except Exception as e:
            print(e)
            self.error = "Errir"





