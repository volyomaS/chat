from django.contrib.auth.models import User
from django.db.models import Model, TextField, DateTimeField, ForeignKey, CASCADE
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class MessageModel(Model):
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField('body')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        new_id = self.id
        self.body = self.body.strip()
        super(MessageModel, self).save(*args, **kwargs)
        if new_id is None:
            self.notify_ws_clients()

    def notify_ws_clients(self):
        notification = {
            'type': 'receive_group_message',
            'message': f'{self.id}'
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'{self.user.id}', notification)
        async_to_sync(channel_layer.group_send)(f'{self.recipient.id}', notification)

    class Meta:
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
