from text_bot.pagination import CustomPagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from text_bot.swagger.textbot_schema import textbot_output_schema, user_history_list_schema, top_chat_list_schema
from .serializers import TextbotOutputSerializer
from rest_framework.viewsets import GenericViewSet
import requests
from api_crud.settings import REACT_APP_TAX3PO_API_DEV_URL, REACT_APP_TAX3PO_API_KEY, TAX3PO_API_ENDPOINT_CONVERSATION
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from text_bot.utils import extract_human_ai_conversation_from_string, get_base64_string
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import UserHistorySerializer
from .serializers import ChatQuestionSerializer
from .models import UserHistory
from django.shortcuts import render, get_object_or_404, redirect
from text_bot.views.models import ChatQuestion
from text_bot.nlp_model.rag.chat_manager import ChatManager
from text_bot.nlp_model.openai_model import OpenaiModel
from text_bot.nlp_model.text_extraction.extraction_manager import ExtractionManager
from text_bot.nlp_model.llama_model import LLamaModel

class TopChatsView(GenericViewSet):

    serializer_class = ChatQuestion
    pagination_class = CustomPagination

    @swagger_auto_schema(
        method="GET",
        responses={
            200: top_chat_list_schema,
            403: "Forbidden",
        },
        tags=["Public chat"],
    )
    @action(methods=["GET"], detail=True)
    def get_top_chats_response(self, request: Request):
        print(request.META)

        top_chats = ChatQuestion.objects.order_by('appearance_count')[:10]
        serializer = ChatQuestionSerializer(top_chats, many=True)
        serialized_data = serializer.data
        return Response({'top_chat_list': serialized_data})


class PublicTextExtractionAPIView(GenericViewSet):
    serializer_class = TextbotOutputSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        method="GET",
        # manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER,
        #                                      description="Token {auth_token}",
        #                                      type=openapi.TYPE_STRING)],
        # request_body=textbot_input_schema,
        responses={
            200: textbot_output_schema,
            403: "Forbidden",
        },
        tags=["Public chat"],
    )
    @action(methods=["GET"], detail=True)
    def get_document_extraction_response(self, request: Request):
        print(request.META)

        extraction_manager = ExtractionManager(LLamaModel())

        document_file_path = request.query_params.get('document_file_path', '')
        # history_key = request.query_params.get('history_key', '')

        response = extraction_manager.process_document(document_file_path)

        if response:
            return Response(response)  # return the data in the DRF Response
        else:
            print("Your request failed")
            return Response(response.json(), status=response.status_code)


class PublicTextBotAPIView(GenericViewSet):
    serializer_class = TextbotOutputSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        method="GET",
        # manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER,
        #                                      description="Token {auth_token}",
        #                                      type=openapi.TYPE_STRING)],
        # request_body=textbot_input_schema,
        responses={
            200: textbot_output_schema,
            403: "Forbidden",
        },
        tags=["Public chat"],
    )
    @action(methods=["GET"], detail=True)
    def get_chat_response(self, request: Request):
        print(request.META)

        chat_manager = ChatManager(OpenaiModel())

        input = request.query_params.get('input', '')
        # history_key = request.query_params.get('history_key', '')

        response = chat_manager.send_user_query(input)

        if response:
            return Response(response)  # return the data in the DRF Response
        else:
            print("Your request failed")
            return Response(response.json(), status=response.status_code)



class TextBotAPIView(GenericViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TextbotOutputSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        method="GET",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER,
                                             description="Token {auth_token}",
                                             type=openapi.TYPE_STRING)],
        # request_body=textbot_input_schema,
        responses={
            200: textbot_output_schema,
            403: "Forbidden",
        },
        tags=["Text bot"],
    )
    @action(methods=["GET"], detail=True)
    def get_chat_response(self, request: Request):
        print(request.META)

        input = request.query_params.get('input', '')
        history_key = request.query_params.get('history_key', '')

        base64_string = get_base64_string(REACT_APP_TAX3PO_API_KEY)

        headers = {'Authorization': "Basic " + base64_string,
                   'Content-Type': 'application/x-www-form-urlencoded'}

        data = {'input': input, 'history_key': history_key}

        response = requests.post(REACT_APP_TAX3PO_API_DEV_URL+TAX3PO_API_ENDPOINT_CONVERSATION, headers=headers, data=data)

        # You may want to check that the request was successful
        if response.status_code == 200:
            data = response.json()  # parse JSON response into a Python dictionary

            new_history_key = data['history_key']

            if new_history_key != history_key:
                UserHistory.objects.create(creator = self.request.user,
                                           history_key = new_history_key)

            buffer = data['buffer']
            buffer = extract_human_ai_conversation_from_string(buffer)
            data['buffer'] = buffer
            return Response(data)  # return the data in the DRF Response
        else:
            print("Your request failed")
            return Response(response.json(), status=response.status_code)

# Retrieve movies view
class UserHistoryListView(GenericViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the user's movie history based on the user's ID
        return UserHistory.objects.filter(creator=self.request.user.id)

    @swagger_auto_schema(
        method="GET",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER,
                                             description="Token {auth_token}",
                                             type=openapi.TYPE_STRING)],
        responses={
            200: user_history_list_schema,
            403: "Forbidden",
        },
        tags=["User history"],
    )
    @action(methods=["GET"], detail=True)
    def get_current_user_history(self, request):
        # Retrieve all movies related to the current user
        current_user_history = UserHistory.objects.filter(creator=request.user.id)
        serializer = UserHistorySerializer(current_user_history, many=True)
        return Response({'user_history_list': serializer.data})

class RetrieveUserHistoryView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserHistorySerializer
    queryset = UserHistory.objects.all()


class DeleteUserHistoryView(GenericViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, history_key):
        # Get the record to be deleted using the primary key (pk)
        record = get_object_or_404(UserHistory, history_key=history_key)

        if request.method == 'POST':
            # If the request method is POST, delete the record and redirect to a success page
            record.delete()
            return redirect('success_page')

        return render(request, 'delete_record.html', {'record': record})

    @swagger_auto_schema(
        method="DELETE",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER,
                                             description="Token {auth_token}",
                                             type=openapi.TYPE_STRING)],
        tags=["User history delete"],
    )
    @action(methods=["DELETE"], detail=True)
    def delete_history_key(self, request, history_key):
        # Get the record to be deleted using the primary key (pk)
        record = UserHistory.objects.filter(history_key=history_key).first()

        # Perform filtering based on the record field value (e.g., 'status')
        if record: # Replace 'status' with your desired field
            # Delete the record if the condition is met
            record.delete()
            return Response({'message': 'Record deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Return an error response if the record is not found or does not meet the condition
            return Response({'message': 'Record not found or cannot be deleted.'}, status=status.HTTP_404_NOT_FOUND)
