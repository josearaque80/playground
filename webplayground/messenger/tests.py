from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message

# Create your tests here.
class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')

        self.thread = Thread.objects.create()

    def test_add_users_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        self.assertEqual(len(self.thread.users.all()), 2)

    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])

    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)

    def test_add_messages_to_thread(self):  # test para agregar mensajes al hilo
        self.thread.users.add(self.user1, self.user2)   # agregamos los usuarios al hilo
        message1 = Message.objects.create(user=self.user1, content='Muy buenas') # mensaje prueba
        message2 = Message.objects.create(user=self.user2, content='Hola')  # mensaje prueba
        self.thread.messages.add(message1, message2)    # agregamos los mensajes al hilo
        self.assertEqual(len(self.thread.messages.all()), 2)    # verificamos que se hayan agregado los mensajes

        for message in self.thread.messages.all():
            print('({}): {}'.format(message.user, message.content)) # imprimimos los mensajes

    def test_add_message_from_user_not_in_thread(self):  # test para agregar mensajes de un usuario que no esta en el hilo
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Muy buenas')
        message2 = Message.objects.create(user=self.user2, content='Hola')
        message3 = Message.objects.create(user=self.user3, content='Soy un espía')
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)    # verificamos que se hayan agregado los mensajes

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, thread)

    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1, self.user2)
        self.assertEqual(self.thread, thread)

        thread = Thread.objects.find_or_create(self.user1, self.user3) # creamos un hilo con un usuario que no esta en el hilo
        self.assertIsNotNone(thread)   # verificamos que el hilo no sea None