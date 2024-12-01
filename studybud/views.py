from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  UserCreationForm
from .forms import MessageForm  





# rooms = [
#     {'id': 1, "name": "Let's Learn Python"},
#     {'id': 2, "name": "Learn Projects"},
#     {'id': 3, "name": "Try new JavaScript"},
# ]

# def loginpage(request):
#      context={}
#      return render(request,"studybud/login_register.html",context)
     
def loginpage(request):
    page='login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password is not exist')
    context={'page':page}

    return render(request, "studybud/login_register.html",context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    
    form= UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request,"studybud/login_register.html",{'form':form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    # Filtering rooms based on the search query 'q'
    rooms = Room.objects.filter(topic__name__icontains=q)

    topics = Topic.objects.all()
    room_messages = Message.objects.all()
    
    context = {"rooms": rooms, 'topics': topics,'room_messages':room_messages}
    return render(request, 'studybud/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    form = MessageForm()  # Initialize the form

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Handle both text and files
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.room = room
            message.save()
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
        'form': form
    }
    return render(request, 'studybud/room.html', context)
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully!')
            return redirect('home')  # Or redirect to a specific room, if desired
    context = {'form': form}
    return render(request, 'studybud/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Your are not allowed')
    if request.method == 'POST':
        form=RoomForm(request.POST,instance=room)
    if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}

    return render(request,'studybud/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=="POST":
          room.delete()
          return redirect('home')
    return render(request, 'studybud/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'studybud/delete.html', {'obj': message})




