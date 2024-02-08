from django.urls import reverse
from django.contrib.auth.models import User


class BypassAuthForSwaggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        swagger_urls = [reverse('schema-swagger-ui'), reverse('schema-redoc')]

        if request.path in swagger_urls:
            request.user = User.objects.get(username='')

        response = self.get_response(request)

        return response