from rest_framework import serializers

from .models import TextingList, Client, Message


class TextingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextingList
        fields = ['id', 'start_datetime', 'end_datetime',
                  'text', 'filter_operator_code', 'filter_tag']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'operator_code', 'tag', 'timezone']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'textinglist', 'client', 'created_at', 'status']
