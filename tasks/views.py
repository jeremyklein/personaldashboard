from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Task, BountyGoal
from .forms import TaskForm, BountyGoalForm
import json


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    
    # Filter options
    status_filter = request.GET.get('status', None)
    priority_filter = request.GET.get('priority', None)
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Create Task',
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            # Check if task status changed to completed
            if task.status == 'completed' and not task.completed_at:
                task.completed_at = timezone.now()
                task.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task,
        'title': 'Update Task',
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task,
    })


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_complete.html', {
        'task': task,
    })


@login_required
def bounty_dashboard(request):
    # Get weekly goal if it exists
    now = timezone.now()
    # Calculate the start of the current week (Monday)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    current_week_goal = BountyGoal.objects.filter(
        user=request.user,
        week_start_date=start_of_week.date()
    ).first()
    
    # Get completed tasks with bounties
    completed_tasks = Task.objects.filter(
        user=request.user,
        status='completed',
        completed_at__isnull=False
    )
    
    # Calculate total bounties
    total_bounties = completed_tasks.aggregate(Sum('bounty'))['bounty__sum'] or 0
    
    # Calculate current week's bounties
    current_week_tasks = completed_tasks.filter(completed_at__gte=start_of_week)
    current_week_bounties = current_week_tasks.aggregate(Sum('bounty'))['bounty__sum'] or 0
    current_week_task_count = current_week_tasks.count()
    
    # Generate data for the weekly velocity chart - last 8 weeks
    weekly_data = []
    week_start = start_of_week - timedelta(days=7*7)  # 7 weeks back
    
    for i in range(8):  # Current week + 7 previous weeks
        week_end = week_start + timedelta(days=7)
        week_tasks = completed_tasks.filter(
            completed_at__gte=week_start,
            completed_at__lt=week_end
        )
        week_bounty = week_tasks.aggregate(Sum('bounty'))['bounty__sum'] or 0
        week_task_count = week_tasks.count()
        
        weekly_data.append({
            'week_start': week_start.date().strftime('%Y-%m-%d'),
            'week_label': week_start.date().strftime('%b %d'),
            'bounty': week_bounty,
            'task_count': week_task_count
        })
        
        week_start = week_end
    
    # Handle creating or updating weekly goal
    if request.method == 'POST':
        form = BountyGoalForm(request.POST, instance=current_week_goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.week_start_date = start_of_week.date()
            goal.save()
            return redirect('bounty_dashboard')
    else:
        form = BountyGoalForm(instance=current_week_goal, initial={'week_start_date': start_of_week.date()})
    
    context = {
        'total_bounties': total_bounties,
        'current_week_bounties': current_week_bounties,
        'current_week_task_count': current_week_task_count,
        'weekly_data': json.dumps(weekly_data),
        'current_week_goal': current_week_goal,
        'goal_form': form,
        'goal_progress': (current_week_bounties / current_week_goal.goal_amount * 100) if current_week_goal else 0,
    }
    
    return render(request, 'tasks/bounty_dashboard.html', context)
