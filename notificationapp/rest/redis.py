from django.utils.dateparse import parse_datetime

import redis


r = redis.Redis(host='localhost', port=6379, db=0)


class TextingListCache:
    FIELD_NAME = ''
    KEY_FORMAT = 'texting-list-{}-{}'

    def set(self, texting_list_id, task_id):
        r.set(self.KEY_FORMAT.format(self.FIELD_NAME, texting_list_id),
              f'{task_id}')

    def get(self, texting_list_id):
        return r.get(self.KEY_FORMAT.format(self.FIELD_NAME,
                                            texting_list_id)).decode()

    def delete(self, texting_list_id):
        r.delete(self.KEY_FORMAT.format(self.FIELD_NAME, texting_list_id))


class TaskIdCache(TextingListCache):
    FIELD_NAME = 'task-id'


class EndDatetimeCache(TextingListCache):
    FIELD_NAME = 'end-date-time'

    def set(self, texting_list_id, end_datetime):
        end_datetime = end_datetime.isoformat()
        return super().set(texting_list_id, end_datetime)

    def get(self, texting_list_id):
        date_parser = super().get(texting_list_id)
        return parse_datetime(date_parser)


task_id_cache = TaskIdCache()
end_datetime_cache = EndDatetimeCache()
