from rest_framework.viewsets import ModelViewSet

from .models import TextingList, Client, Message
from .serializers import TextingListSerializer, ClientSerializer, MessageSerializer


class TextingListViewSet(ModelViewSet):
    queryset = TextingList.objects.all()
    serializer_class = TextingListSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    
class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer