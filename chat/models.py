from django.contrib.auth.models import User
from django.db.models import Model, TextField, DateTimeField, ForeignKey, CASCADE
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class MessageModel(Model):
    """
    Message database model class
    """
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField('body')

    # TODO may be deleted?
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        Overriding Model.save() function
        Now it notifies consumers using websocket
        if this message is new
        """
        new_id = self.id
        self.body = self.body.strip()
        super(MessageModel, self).save(*args, **kwargs)
        if new_id is None:
            self.notify_ws_clients()

    def notify_ws_clients(self):
        """
        Notifying consumers about new message using websocket
        """
        notification = {
            'type': 'receive_group_message',
            'message': f'{self.id}'
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'{self.user.id}', notification)
        async_to_sync(channel_layer.group_send)(f'{self.recipient.id}', notification)

    class Meta:
        """
        Meta class with properties
        """
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
