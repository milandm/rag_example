from django.urls import path
from . import views


urlpatterns = [
    path('document-extraction', views.PublicTextExtractionAPIView.as_view({"get": "get_document_extraction_response"}), name='document_extraction_response'),
    path('public-chat', views.PublicTextBotAPIView.as_view({"get": "get_chat_response"}), name='chat_response'),
    path('', views.TextBotAPIView.as_view({"get": "get_chat_response"}), name='chat_response'),
    path('user-history-keys', views.UserHistoryListView.as_view({"get": "get_current_user_history"}), name='current_user_history'),
    path('top-chats', views.TopChatsView.as_view({"get": "get_top_chats_response"}), name='top_chats'),
    path('user-history-keys/delete/<str:history_key>/', views.DeleteUserHistoryView.as_view({"delete": "delete_history_key"}), name='delete_user_history'),
]