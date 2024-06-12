from .models import User, Room
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse # new import for testing views with url parameters

class TestUserProfile(TestCase):
     def setUp(self):
          self.client = Client()

          self.user = User.objects.create(
               email='test@mail.ru',
               password='12345'
          )
          self.client.login(email='test@mail.ru', password='12345')

     # def test_user_profile_GET(self):
     #      print(self.user.email)  # Debug line
     #      print(get_user_model().objects.all())  # Debug line
     #      response = self.client.get(reverse('userprofile', args=['test@mail.ru']))
     #      self.assertEqual(response.status_code, 200)
     #      self.assertTemplateUsed(response, 'base/profile.html')

     def test_createRoom_POST(self):
          response = self.client.post(reverse('newroom'), {
               'name': 'Test Room',
               'description': 'This is a test room.',
               'topic': 'Test Topic'
          })
          self.assertEqual(response.status_code, 302)
          self.assertEqual(Room.objects.get(name='Test Room'), 'Test Room')