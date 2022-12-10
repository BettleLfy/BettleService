from django.db import models
import pytz


# blank=False, default=None, null=False
class TextingList(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    text = models.TextField()
    filter_operator_code = models.PositiveIntegerField()
    filter_tag = models.CharField(max_length=100)

    def __str__(self):
        return (f'{self.text[:20]} '
                f'({self.filter_operator_code}), '
                f'#{self.filter_tag}')


class Client(models.Model):
    phone = models.PositiveIntegerField()
    operator_code = models.PositiveIntegerField()
    tag = models.CharField(max_length=100)
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES,
                                default='Europe/Moscow')

    def __str__(self):
        return str(self.phone)


class Message(models.Model):
    PENDING = 'PENDING'
    SENT = 'SENT'
    CURRENT_STATUS = [(PENDING, 'Pending'),
                      (SENT, 'Sent')]
    textinglist = models.ForeignKey(TextingList,
                                    on_delete=models.CASCADE,
                                    related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=CURRENT_STATUS,
                              default=PENDING)
