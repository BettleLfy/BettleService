from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from taskqueue.tasks import notify_texting_list
from notificationapp import celery_app

from .models import TextingList, Client, Message
from .redis import end_datetime_cache, task_id_cache
from .serializers import (TextingListSerializer,
                          ClientSerializer,
                          MessageSerializer)


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

    def start_task(self, texting_list):
        instance = texting_list
        if instance.start_datetime < timezone.now():
            task = notify_texting_list.delay(instance.id)
        else:
            task = notify_texting_list.apply_async(args=[instance.id],
                                                   eta=instance.start_datetime)
        task_id_cache.set(instance.id, task.id)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        end_datetime_cache.set(instance.id, instance.end_datetime)
        self.start_task(instance)

    def perform_update(self, serializer):
        instance = serializer.instance
        start_datetime = instance.start_datetime
        end_datetime = instance.end_datetime
        super().perform_update(serializer)
        if end_datetime != instance.end_datetime:
            end_datetime_cache.set(instance.id, instance.end_datetime)
        if start_datetime > timezone.now():
            task_id = task_id_cache.get(instance.id)
            celery_app.control.revoke(task_id, terminate=True)
            self.start_task(instance)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
