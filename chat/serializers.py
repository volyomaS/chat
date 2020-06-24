from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chat.models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField


class MessageModelSerializer(ModelSerializer):
    """
    Serializer for messages
    """
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        # Getting user from context
        user = self.context['request'].user

        # Getting recipient from db or raising http404
        recipient = get_object_or_404(User, username=validated_data['recipient']['username'])

        # Creating and saving message
        message = MessageModel(user=user, recipient=recipient, body=validated_data['body'])
        message.save()
        return message

    class Meta:
        """
        Meta class with properties
        """
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
