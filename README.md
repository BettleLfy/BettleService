# BettleService
### Description
Сервис для отправки сообщений клиентам в определенный промежуток времени,
используя связку Django Rest Framework/Celery/Redis

### Tech
- Python 3.10
- Django 4.1.3
- Redis 4.4.0
- Celery 5.2.7
- djangorestframework 3.14.0

### Как запустить проект?
- Клонировать данный репозиторий
- установить виртуальное окружение и активировать его
- установить необходимые компоненты с помощью:
```pip install -r requirements.txt```
- В корневой папке(где находится settings.py) 'notificationapp' создать файл '.env' и записать в него секретный ключ, к примеру:
```SECRET_KEY = awduaw123huhanj65o785lz```
- В папке 'taskqueue' так же добавить файл '.env' и написать в него JWT токет, к примеру:
```JWT=djdjasnytjk31m```
- Сделать миграции в БД с помощью:
```python manage.py migrate```
- В данном случае используется WSL для активации Redis, поэтому запустив WSL модуль, необходимо его запустить:
```sudo service redis-server start```
- Для активации Celery, необходимо в консоли ввести команду:
```celery -A notificationapp  worker -l INFO -P threads```
- После запуска всех необходимых сервисов, можно запустить сам django server:
```python manage.py runserver```
- Перейти на [localhost](http://127.0.0.1:8000/api)
- Создать тестового Client
- При создании TextingList указать валидные текст, тег и код оператора и указать корректные даты
- Если все сделано правильно в терминале Celery запустится сделанный вами task и во вкладе Message на странице localhost появится ваше сообщение
