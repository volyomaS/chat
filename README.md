# Chat async module using Django, Channels and REST frameworks
Message model defined in chat/models.py

REST API defined in chat/api.py

Serializers for REST defined in chat/serializers.py

# How to start chat server

1) Start the Redis server on the port that is declared in settings.py like:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```
I did this with docker:

```ps1
docker run -p 6379:6379 -d redis:5
```

2) Create a table in the database for MessageModel. I did it with this command:

```cmd
python manage.py --run-syncdb
```

3) Run the server

```cmd
python manage.py runserver
```
