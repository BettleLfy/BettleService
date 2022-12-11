from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from notificationapp.celery import debug_task
from datetime import datetime, timedelta

from .models import TextingList, Client, Message
from .serializers import (TextingListSerializer,
                          ClientSerializer,
                          MessageSerializer)


class Test(APIView):
    def post(self, request):
        tomorrow = datetime.utcnow() + timedelta(seconds=20)
        debug_task.apply_async(eta=tomorrow)
        return Response({'vanya': 'popa'})


class TextingListViewSet(ModelViewSet):
    queryset = TextingList.objects.all()
    serializer_class = TextingListSerializer

    def calculate_statistics(self, messages):
        messages_status = messages.values('status').annotate(
            count=Count('status'))
        result = {i['status']: i['count'] for i in messages_status}
        for empty, _ in Message.CURRENT_STATUS:
            result.setdefault(empty, 0)
        result['total'] = messages.count()
        return result

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        result = self.calculate_statistics(Message.objects.all())
        return Response(result)

    @action(detail=True, methods=['get'],
            url_path='statistics',
            name='Statistics')
    def statistics_detail(self, request, pk):
        result = self.calculate_statistics(self.get_object().messages.all())
        return Response(result)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
