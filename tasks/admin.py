from django.contrib import admin
from .models import Task, BountyGoal

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'status', 'bounty', 'due_date', 'completed_at')
    list_filter = ('status', 'priority', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(BountyGoal)
class BountyGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_start_date', 'goal_amount')
    list_filter = ('user',)
    date_hierarchy = 'week_start_date'
