from django.utils import timezone

from celery import shared_task

from rest.models import Client, Message, TextingList
from .notification import notify_client
from rest.redis import end_datetime_cache, task_id_cache


@shared_task
def notify_texting_list(texting_list_id):
    try:
        texting_list = TextingList.objects.get(pk=texting_list_id)
        clients = Client.objects.all()
        if texting_list.filter_operator_code is not None:
            clients = clients.filter(
                operator_code=texting_list.filter_operator_code)
        if texting_list.filter_tag != '':
            clients = clients.filter(
                tag=texting_list.filter_tag)
        for client in clients:
            if timezone.now() > get_texting_list_end(texting_list_id):
                raise Exception('Message list has been ended prematurely')
            message = Message.objects.create(
                textinglist=texting_list,
                client=client,
                status=Message.PENDING
            )
            notify_client(message.id, texting_list.text, client.phone)
            message.status = Message.SENT
            message.save()
    finally:
        task_id_cache.delete(texting_list_id)
        end_datetime_cache.delete(texting_list_id)


def get_texting_list_end(texting_list_id):
    return end_datetime_cache.get(texting_list_id)
