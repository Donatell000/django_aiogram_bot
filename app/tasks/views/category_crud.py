from rest_framework.views import APIView

from tasks.services import CategoryCrudService


class CategoryCrudAPIView(APIView):
    def get(self, request):
        service = CategoryCrudService()
        return service.handle_category_get(request)

    def post(self, request):
        service = CategoryCrudService()
        return service.handle_category_post(request)
