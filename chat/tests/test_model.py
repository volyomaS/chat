from django.db import IntegrityError
from django.test import TestCase
from chat.models import MessageModel
from django.contrib.auth.models import User


class MessageTestCase(TestCase):
    """
    Tests checking MessageModel functionality
    """

    def setUp(self):
        """
        Creating users
        """
        self.test_user1 = User.objects.create(username='bart')
        self.test_user2 = User.objects.create(username='milhouse')

    def test_message_user(self):
        """
        Checking MessageModel.user correctness
        """
        msg = MessageModel.objects.create(user=self.test_user2,
                                          recipient=self.test_user1,
                                          body='test')
        self.assertEqual(msg.user.username, 'milhouse')

    def test_message_body(self):
        """
        Checking MessageModel.body correctness
        """
        msg = MessageModel.objects.create(user=self.test_user1,
                                          recipient=self.test_user2,
                                          body='123')
        self.assertEqual(msg.body, '123')

    def test_message_body_strip(self):
        """
        Checking MessageModel.body strip correctness
        """
        msg = MessageModel.objects.create(user=self.test_user1,
                                          recipient=self.test_user2,
                                          body=' aaa ')
        self.assertEqual(msg.body, 'aaa')

    def test_message_no_user(self):
        """
        Checking impossibility of creating MessageModel without User
        """
        with self.assertRaises(IntegrityError):
            MessageModel.objects.create(user=None, body='test')

    def test_message_create_retrieve(self):
        """
        Checking MessageModel retrieval
        """
        mid = MessageModel.objects.create(user=self.test_user1,
                                          recipient=self.test_user2,
                                          body='tbody').id
        msg = MessageModel.objects.get(id=mid)

        self.assertEqual(msg.body, 'tbody')
        self.assertEqual(msg.user, self.test_user1)
        self.assertEqual(msg.recipient, self.test_user2)
