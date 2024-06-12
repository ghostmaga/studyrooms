from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Room, Topic, Message, User
from .forms import RoomForm, MessageForm, UserForm, CustomUserCreationForm
# Create your views here.

def login_page(request):
     if request.user.is_authenticated:
          return redirect('home')
     if request.method == 'POST':
          email = request.POST.get('email').lower()
          password = request.POST.get('password')
          try:
               user = User.objects.get(email=email)
          except:
               messages.error(request, 'User with provided username does not exist. Please register.')

          user = authenticate(request, email=email, password=password)
          if user is not None:
               login(request, user)
               return redirect('home')
          else:
               messages.error(request, 'Username or Password is incorrect.')

     context = {}
     return render(request, 'base/login.html', context)

def register_page(request):
     form = CustomUserCreationForm()

     if request.method == 'POST':
          form = CustomUserCreationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.username = user.username.lower()
               user.save()
               login(request, user)
               return redirect('home')
          else:
               if 'password2' in form.errors.as_data():
                    messages.error(request, 'Passwords do not match.') 
               elif 'email' in form.errors.as_data():
                    messages.error(request, 'Email already exists.') 
               else:
                    messages.error(request, 'An error occurred during the registration. Please try again later.')

     return render(request, 'base/signup.html', {'form': form})

def logout_user(request):

     logout(request)
     return redirect('login')

def user_profile(request, email):
     user = User.objects.get(email=email)
     rooms = user.room_set.all()
     roommessages = user.message_set.all()
     topics = Topic.objects.all().filter(room__host=user)

     allTopicsCount = 0
     for topic in topics:
          allTopicsCount += topic.room_set.count()
          print(topic.room_set.all())

     context = {'user':user, 'rooms':rooms, 'roommessages':roommessages, 'topics':topics, 'total': allTopicsCount}
     return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def update_user(request, username):
     if request.user.email != username:
          return HttpResponse('You do not have access to this page.')
     
     user = request.user
     form = UserForm(instance=user)

     if request.method == 'POST':
          form = UserForm(request.POST, request.FILES, instance=user)
          if form.is_valid():
               form.save()
               return redirect('userprofile', request.user.email)
     context = {'form': form}
     return render(request, 'base/update-user.html', context)

def home(request):
     q = request.GET.get('q') if request.GET.get('q') != None else ''

     studyrooms = Room.objects.all().filter(

          Q(topic__name__icontains=q) | 
          Q(name__icontains=q) |
          Q(description__icontains=q)
          
     ) if q else Room.objects.all()

     rooms_count = studyrooms.count()
     topicsList = Topic.objects.all()[0:5]
     allTopicsCount = 0
     for topic in topicsList:
          allTopicsCount += topic.room_set.count()
          print(topic.room_set.all())

     roommessages = Message.objects.filter(
          Q(room__topic__name__icontains=q)
     )[:20]

     context = {'rooms': studyrooms, 'topics': topicsList, 'rooms_count': rooms_count, 'roommessages': roommessages, 'total': allTopicsCount}
     return render(request, 'base/home.html', context)

def room(request, roomid):
     room = Room.objects.get(id=roomid)
     participants = room.participants.all()
     if request.method == 'POST':
          message = Message.objects.create(
               user=request.user,
               room=room,
               body=request.POST.get('commentbody')
          )
          message.save()
          room.participants.add(request.user)
          return redirect('room', roomid=roomid)

     messagesList = Message.objects.filter(room=room)
     context = {'room': room, 'roommessages': messagesList, 'participants': participants}
     return render(request, 'base/room.html', context)

def topic(request, topicid):
     rooms = Room.objects.filter(topic=topicid)
     context = {'rooms': rooms}

     return render(request, 'base/home.html', context)

@login_required(login_url='login')
def createRoom(request):
     form = RoomForm()
     topicsList = Topic.objects.all()

     if request.method == 'POST':
          topic_name = request.POST.get('topic').lower().capitalize()
          topic, created = Topic.objects.get_or_create(name=topic_name)

          Room.objects.create(
               host=request.user,
               topic=topic,
               name=request.POST.get('name'),
               description=request.POST.get('description')
          )

          return redirect('home')
     context = {'form':form, 'type':'create', 'topics':topicsList}
     return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, roomid):
     room = Room.objects.get(id=roomid)
     if request.user != room.host:
          return HttpResponse('You are not allowed to update this room.')
     
     topicsList = Topic.objects.all()
     form = RoomForm(instance=room)
     
     if request.method == 'POST':
          topic_name = request.POST.get('topic')
          topic, created = Topic.objects.get_or_create(name=topic_name)
          room.name = request.POST.get('name')
          room.description = request.POST.get('description')
          room.topic = topic
          room.save()
          return redirect('home')
     context = {'form':form, 'room': room, 'type':'update', 'topics':topicsList}
     return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, roomid):

     room = Room.objects.get(id=roomid)

     if request.user != room.host:
          return HttpResponse('You are not allowed to delete this room.')
     
     if request.method == 'POST':
          room.delete(keep_parents=True)
          return redirect('home')
     context = {'roomid':roomid, 'object':room}
     return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def editComment(request, messageid):
     message = Message.objects.get(id=messageid)

     if request.user != message.user:
          return HttpResponse('You are not allowed to edit this comment.')

     form = MessageForm(instance=message)
     if request.method == 'POST':
          form = MessageForm(request.POST, instance=message)
          if form.is_valid():
               form.save()
               return redirect('room', roomid=message.room.id)
     context = {'form': form, 'message':message}
     return render(request, 'base/editcomment.html', context)

@login_required(login_url='login')
def deleteComment(request, messageid):

     message = Message.objects.get(id=messageid)

     if request.user != message.user:
          return HttpResponse('You are not allowed to delete this comment.')

     if request.method == 'POST':
          message.delete(keep_parents=True)
          return redirect('room', roomid=message.room.id)
     context = {'object':message, 'roomid':message.room.id}
     return render(request, 'base/delete.html', context)