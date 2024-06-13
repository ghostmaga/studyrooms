from .models import User, Room
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse # new import for testing views with url parameters

class sampleTest(TestCase):

     def testRoomCreation(self):
          roomhost = User.objects.create(
               email='sampleemail@mail.ru',
               password='Qqwe123!'
          )
          room = Room.objects.create(
               name='SampleRoom',
               description='This is a test room.',
               host=roomhost,
          )
          room1 = Room.objects.get(name='SampleRoom')
          self.assertEqual(room1.name, 'SampleRoom')







     # def setUp(self):
     #      self.client = Client()

     #      self.user = User.objects.create(
     #           email='test@mail.ru',
     #           password='12345'
     #      )
     #      self.client.login(email='test@mail.ru', password='12345')

     # def test_createRoom_POST(self):
     #      response = self.client.post(reverse('newroom'), {
     #           'name': 'Test Room',
     #           'description': 'This is a test room.',
     #           'topic': 'Test Topic'
     #      })
     #      self.assertEqual(response.status_code, 302)
     #      self.assertEqual(Room.objects.get(name='Test Room'), 'Test Room')