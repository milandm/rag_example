
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from text_bot.views.text_bot_views import chatbot_demo
from django.conf import settings
from django.conf.urls.static import static


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


# urlpatterns = [
#
#     path('document-extraction', views.PublicTextExtractionAPIView.as_view({"get": "get_document_extraction_response"}), name='document_extraction_response'),
#     path('public-chat', views.PublicTextBotAPIView.as_view({"get": "get_chat_response"}), name='chat_response'),
#     path('sales-agent_public-chat', views.PublicSlesAgentAPIView.as_view({"get": "get_chat_response"}), name='chat_response'),
#     path('', views.TextBotAPIView.as_view({"get": "get_chat_response"}), name='chat_response'),
#     path('user-history-keys', views.UserHistoryListView.as_view({"get": "get_current_user_history"}), name='current_user_history'),
#     path('top-chats', views.TopChatsView.as_view({"get": "get_top_chats_response"}), name='top_chats'),
#     path('user-history-keys/delete/<str:history_key>/', views.DeleteUserHistoryView.as_view({"delete": "delete_history_key"}), name='delete_user_history'),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)