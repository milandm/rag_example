from drf_yasg import openapi

textbot_input_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "input": openapi.Schema(type=openapi.TYPE_STRING),
        "history_key": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

textbot_output_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "output": openapi.Schema(type=openapi.TYPE_STRING),
        "history_key": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

user_history_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "history_key": openapi.Schema(type=openapi.TYPE_STRING),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

user_history_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "user_history_list": user_history_schema,
    },
)


top_chat_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "history_key": openapi.Schema(type=openapi.TYPE_STRING),
        "appearance_count": openapi.Schema(type=openapi.TYPE_INTEGER),
        "text": openapi.Schema(type=openapi.TYPE_STRING),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

top_chat_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "top_chat_list": top_chat_schema,
    },
)