import redis


r = redis.Redis(host='localhost', port=6379, db=0)


class TaskIdCache:

    KEY_FORMAT = 'texting-list-task-id-{}'

    def set(self, texting_list_id, task_id):
        r.set(self.KEY_FORMAT.format(texting_list_id), f'{task_id}')

    def get(self, texting_list_id):
        r.get(self.KEY_FORMAT.format(texting_list_id))

    def delete(self, texting_list_id):
        r.delete(self.KEY_FORMAT.format(texting_list_id))


task_id_cache = TaskIdCache()
