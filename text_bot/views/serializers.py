from rest_framework import serializers
from text_bot.views.models import TextbotOutput, UserHistory, ChatQuestion
from django.contrib.auth.models import User

# const
# url = process.env.REACT_APP_TAX3PO_API_DEV_URL;
# const
# headers = new
# Headers();
# headers.set(
#     "Authorization",
#     "Basic " + Base64.encode(process.env.REACT_APP_TAX3PO_API)
# );
# headers.set("Content-Type", "application/x-www-form-urlencoded");
#
# const
# fetchGPTData = async (data: URLSearchParams) = > {
# return await fetch(url, {
#     method: "POST",
#     headers: headers,
#     body: data,
# });
# };
#
# { input: searchQuery, history_key: historyKey }

class TextbotOutputSerializer(serializers.Serializer):
    output = serializers.ReadOnlyField()

    class Meta:
        model = TextbotOutput
        fields = ('history_key', 'output')

class UserHistorySerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = UserHistory
        fields = ('history_key', 'creator', 'created_at')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    history_keys = serializers.PrimaryKeyRelatedField(many=True, queryset=UserHistory.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'history_keys')


class ChatQuestionSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = ChatQuestion
        fields = ('history_key', 'appearance_count','text', 'created_at')


class ChatQuestionSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = ChatQuestion
        fields = ('history_key', 'appearance_count','text', 'created_at')