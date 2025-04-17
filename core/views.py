from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .forms import UserRegistrationForm
from tasks.models import Task, BountyGoal

@login_required(login_url='login')
def dashboard(request):
    # Get bounty stats for the dashboard
    now = timezone.now()
    
    # Calculate the start of the current week (Monday)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get current week's goal
    current_week_goal = BountyGoal.objects.filter(
        user=request.user,
        week_start_date=start_of_week.date()
    ).first()
    
    # Get completed tasks
    completed_tasks = Task.objects.filter(
        user=request.user,
        status='completed',
        completed_at__isnull=False
    )
    
    # Calculate total bounties
    total_bounties = completed_tasks.aggregate(Sum('bounty'))['bounty__sum'] or 0
    
    # Calculate current week bounties
    current_week_tasks = completed_tasks.filter(completed_at__gte=start_of_week)
    current_week_bounties = current_week_tasks.aggregate(Sum('bounty'))['bounty__sum'] or 0
    current_week_task_count = current_week_tasks.count()
    
    # Get upcoming tasks (not completed, due date in the future)
    upcoming_tasks = Task.objects.filter(
        user=request.user,
        status__in=['not_started', 'in_progress'],
        due_date__isnull=False,
        due_date__gte=now.date()
    ).order_by('due_date')[:5]  # Get 5 nearest upcoming tasks
    
    context = {
        'total_bounties': total_bounties,
        'current_week_bounties': current_week_bounties,
        'current_week_task_count': current_week_task_count,
        'current_week_goal': current_week_goal,
        'upcoming_tasks': upcoming_tasks,
        'goal_progress': int((current_week_bounties / current_week_goal.goal_amount * 100) if current_week_goal and current_week_goal.goal_amount > 0 else 0),
    }
    
    return render(request, 'core/dashboard.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
