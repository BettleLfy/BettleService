from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TextingList, Client, Message
from .serializers import (TextingListSerializer,
                          ClientSerializer,
                          MessageSerializer)


class TextingListViewSet(ModelViewSet):
    queryset = TextingList.objects.all()
    serializer_class = TextingListSerializer

    def calculate_statistics(self, messages):
        messages_stats = messages.count()
        messages_sent = messages.filter(status=Message.SENT).count()
        messages_pending = messages.filter(status=Message.PENDING).count()
        return {'total': messages_stats,
                'sent': messages_sent,
                'pending': messages_pending}

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
