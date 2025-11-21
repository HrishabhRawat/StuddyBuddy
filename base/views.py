from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate , login, logout
from .models import Room, Topic, Message, User 
from .forms import RoomForm, UserForm, MyUserCreationForm


# For login page
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:                   # if a user is logged in he cannot access it
        return redirect('home')
    if request.method == 'POST':                                # getting the username and password
        email = request.POST.get('email').lower()               # from the login form that we have created
        password = request.POST.get('password')
        try:                                                    # checking if the user exist 
            user = User.objects.get(email= email)
        except:
            messages.error(request , 'User does not exist')
        user = authenticate(request, email= email , password= password)     # if the user exist authenticating user
                                                                                  # making sure that all the credentials
                                                                                  # are correct

        if user is not None:                                # logining a user and redirecting it to home page
            login(request , user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

# register view
def registerPage(request):
    form = MyUserCreationForm()    # using built in form for registering a user

    if request.method == 'POST':            # we pass in the user data
        form = MyUserCreationForm(request.POST)           # throw that data in the user creation form
        if form.is_valid():                 # checking if the form is valid
            user = form.save(commit=False)          
            user.username = user.username.lower()       # getting in the username in lowercase
            user.save()         # save the user 
            login(request, user)                # logged the user in
            return redirect('home')             # redirecting the user back to home template
        else:
            messages.error(request, 'An Error occured during registration')
            
    return render(request, 'base/login_register.html', {'form': form})

# logout view
def logoutUser(request):
    logout(request)
    return redirect('home')

# home view
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |   
                                Q(name__icontains=q)|
                                Q(description__icontains=q)
                                )     
    topics = Topic.objects.all()[0:5]   
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains= q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages':room_messages}    
    return render(request , 'base/home.html', context)


# room view
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()  # give us the set of messages that are related to this specific room
    participants = room.participants.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)


# profile view
def userProfile(request, pk):
    user = User.objects.get(id= pk)
    rooms = user.room_set.all()       # this will get child objects data
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context ={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

# createRoom view
@login_required(login_url='login')      # restricing user to create room without logining in
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':       # send the post data
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic= topic,
            name= request.POST.get('name'),
            description= request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

# updateRoom view
@login_required(login_url='login')    # restricting user to update room without logining in
def updateRoom(request, pk):   # passing primary key to know what item we want to update
    room = Room.objects.get(id= pk)    # getting the item that we want to update
    form = RoomForm(instance= room)    # what will do it we prefill the the form for us to update 
    topics = Topic.objects.all()
    if request.user != room.host:                            # this will not allow different user to update room
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')         # redirect the user back to home page
        
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)
    
# delete room view 
@login_required(login_url='login')          # restricting user to delete room without logining in
def deleteRoom(request, pk):
    room = Room.objects.get(id= pk) 
    if request.user != room.host:                    # this will not allow different user to delete room
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete()      
        return redirect('home')
    return render(request ,'base/delete.html', {'obj': room} )

# delete message view
@login_required(login_url='login')          # restricting user to delete message without logining in
def deleteMessage(request, pk):
    message = Message.objects.get(id= pk)        # getting a message
    if request.user != message.user:                    
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        message.delete()      
        return redirect('home')
    return render(request ,'base/delete.html', {'obj': message} )

# update user view
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES,  instance= user ) 
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form':form}
    return render(request, 'base/update-user.html', context)


# view for topics page
def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


# view for activities
def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)
