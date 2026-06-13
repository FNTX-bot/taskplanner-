from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TaskForm
from .models import Task


@login_required
def dashboard(request):
    filter_type = request.GET.get('filter', 'all')
    qs = Task.objects.filter(user=request.user)

    if filter_type == 'today':
        qs = qs.filter(due_datetime__date=timezone.localdate())
    elif filter_type == 'pending':
        qs = qs.filter(is_done=False)
    elif filter_type == 'done':
        qs = qs.filter(is_done=True)

    total = Task.objects.filter(user=request.user).count()
    done_count = Task.objects.filter(user=request.user, is_done=True).count()
    progress = int((done_count / total) * 100) if total else 0

    # Reminders: undone tasks whose reminder window has opened
    reminder_list = [
        t for t in Task.objects.filter(user=request.user, is_done=False)
        if t.needs_reminder()
    ]

    return render(request, 'tasks/dashboard.html', {
        'tasks': qs,
        'filter_type': filter_type,
        'total': total,
        'done_count': done_count,
        'progress': progress,
        'reminder_list': reminder_list,
    })


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created.')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit'})


@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.is_done = not task.is_done
        task.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
    return redirect('dashboard')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                form.add_error('username', 'A user with that username already exists.')
            else:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
