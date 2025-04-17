from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    bounty = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def mark_completed(self):
        if self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()
            
    class Meta:
        ordering = ['-created_at']


class BountyGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bounty_goals')
    week_start_date = models.DateField()
    goal_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Goal for week of {self.week_start_date}: {self.goal_amount} bounties"
    
    class Meta:
        unique_together = ('user', 'week_start_date')
