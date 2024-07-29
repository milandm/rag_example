
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from text_bot.views.text_bot_views import chatbot_demo


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema.basePath = "/api/v1"  # API prefix
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Application IR",
        default_version="api_crud",
        description="Application endpoints",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=CustomOpenAPISchemaGenerator,
    patterns=[
        path("", include("api_crud.urls")),
    ],
)

# urls
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(
        "swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path("docs/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/textbot/', include('text_bot.urls')),
    path('admin/', admin.site.urls),

    path('chatbot-demo/', chatbot_demo, name='chatbot_demo'),
]