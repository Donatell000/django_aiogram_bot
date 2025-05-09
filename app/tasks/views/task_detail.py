from rest_framework.views import APIView
from rest_framework.response import Response

from tasks.services import TaskDetailService


class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        service = TaskDetailService(pk)
        return Response(service.get_task_data())

    def put(self, request, pk):
        service = TaskDetailService(pk, data=request.data)
        return service.update_task()

    def patch(self, request, pk):
        service = TaskDetailService(pk, data=request.data)
        return service.patch_task()

    def delete(self, request, pk):
        service = TaskDetailService(pk, data=request.data)
        return service.delete_task()
