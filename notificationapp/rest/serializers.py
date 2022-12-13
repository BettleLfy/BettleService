from rest_framework import serializers
from django.utils import timezone

from .models import TextingList, Client, Message


class TextingListSerializer(serializers.ModelSerializer):
    def validate_end_datetime(self, end_datetime):
        if end_datetime < timezone.now():
            raise serializers.ValidationError('Дата окончания не может '
                                              'быть в прошлом')
        return end_datetime

    def validate(self, attrs):
        end_datetime = attrs.get('end_datetime')
        start_datetime = attrs.get('start_datetime')
        if start_datetime > end_datetime:
            raise serializers.ValidationError(
                {'end_datetime': 'Дата окончания должна быть позже начала'},
            )
        obj = self.instance
        if obj is not None:
            if (obj.start_datetime <= timezone.now() <= obj.end_datetime
                    and obj.start_datetime != start_datetime):
                raise serializers.ValidationError(
                    {'start_datetime': 'Невозможно изменить дату'
                                       ' начала начавшегося задания'},
                )
        return attrs

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
