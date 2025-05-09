from rest_framework.views import APIView

from tasks.services import CategoryDetailService


class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        service = CategoryDetailService(request)
        return service.get(pk)

    def put(self, request, pk):
        service = CategoryDetailService(request)
        return service.put(pk)

    def delete(self, request, pk):
        service = CategoryDetailService(request)
        return service.delete(pk)
