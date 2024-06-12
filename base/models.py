from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Django User model fields:
# username
# password
# email
# first_name
# last_name
# is_staff
# is_active
# date_joined
# last_login

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
     name = models.CharField(max_length=100, unique=True)

     def __str__(self):
          return self.name
     
     def delete(self, *args, **kwargs):
        others_topic, created = Topic.objects.get_or_create(name='Others')
        Room.objects.filter(topic=self).update(topic=others_topic)
        super().delete(*args, **kwargs)

class Room(models.Model):
     host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

     name = models.CharField(max_length=100)
     description = models.TextField(null=True, blank=True)
     participants = models.ManyToManyField(User, related_name='participants', blank=True)
     
     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     # NOW using the default id field that django provides

     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

     class Meta():
          ordering = ['-updated', '-created']

     def __str__(self):
          return self.name
     
class Message(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     room = models.ForeignKey(Room, on_delete=models.CASCADE)
     body = models.TextField()

     updated = models.DateTimeField(auto_now=True)
     created = models.DateTimeField(auto_now_add=True)

     class Meta():
          ordering = ['-created']

     def __str__(self):
          return self.body[0:50]