from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Participant, Ticket, Task
from .forms import EventForm, ParticipantForm, TaskForm
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import EmailForm

@login_required
def event_list(request):
    events = Event.objects.all().order_by('date', 'time')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tasks = Task.objects.filter(event=event)
    is_owner = request.user == event.created_by
    task_form = TaskForm() if is_owner else None
    return render(request, 'events/event_detail.html', {
        'event': event,
        'tasks': tasks,
        'is_owner': is_owner,
        'form': task_form
    })

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def participant_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.event = event
            participant.save()
            ticket = Ticket.objects.create(participant=participant, event=event)
            send_mail(
                'Your Ticket',
                f'Thank you for registering. Your ticket ID is {ticket.id}.',
                'amir.aezzi2019@gmail.com',
                [participant.email],
                fail_silently=False,
            )
            return redirect('event_detail', event_id=event.id)
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form, 'event': event})

@login_required
def task_create(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.created_by:
        return redirect('event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.event = event
            task.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = TaskForm()
    
    return render(request, 'events/task_form.html', {'form': form, 'event': event})
@login_required
def send_task_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.created_by:
        return redirect('event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            tasks = Task.objects.filter(event=event)
            task_list = "\n".join([task.description for task in tasks])
            send_mail(
                f'Task List for {event.title}',
                f'Tasks:\n{task_list}',
                'amir.aezzi2019@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('event_detail', event_id=event.id)
    else:
        form = EmailForm()

    return render(request, 'events/send_task_list.html', {'form': form, 'event': event})
@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.event.created_by:
        if request.method == 'POST':
            task.completed = request.POST.get('completed') == 'on'
            task.save()
    return redirect('event_detail', event_id=task.event.id)

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('event_list')


@login_required
def participant_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.created_by:
        # If the user is not the owner, redirect or show an error
        return redirect('event_detail', event_id=event_id)
    
    participants = Participant.objects.filter(event=event)
    return render(request, 'events/participant_list.html', {'event': event, 'participants': participants})