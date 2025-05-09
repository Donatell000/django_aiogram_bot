from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.services import TaskCrudService


class TaskCrudAPIView(APIView):
    def get(self, request) -> Response:
        service = TaskCrudService(request)
        response_data, status_code = service.handle_get()
        return Response(response_data, status=status_code)

    def post(self, request) -> Response:
        service = TaskCrudService(request)
        response_data, status_code = service.handle_post()
        return Response(response_data, status=status_code)
