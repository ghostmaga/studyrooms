#URL config
#every app has its own url conf file
#URLs are mapped to view functions
#then must be included in the project's(MAIN) url conf

from django.urls import path
from . import views

urlpatterns = [
     path('login/', views.login_page, name='login'),
     path('logout/', views.logout_user, name='logout'),
     path('register/', views.register_page, name='register'),

     path('userprofile/<str:email>/', views.user_profile, name='userprofile'),
     path('updateuser/<str:username>', views.update_user, name='updateuser'),

     path('', views.home, name='home'),
     
     path('topics/topic/<str:topicid>/', views.topic, name='topic'),

     path('room/<str:roomid>/', views.room, name='room'),
     path('new-room/', views.createRoom, name='newroom'),
     path('update-room/<str:roomid>/', views.updateRoom, name='updateroom'),
     path('delete/<str:roomid>/', views.deleteRoom, name='delete'),

     path('editcomment/<str:messageid>/', views.editComment, name='editcomment'),
     path('deletecomment/<str:messageid>/', views.deleteComment, name='deletecomment'),
]