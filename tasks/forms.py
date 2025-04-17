from django import forms
from .models import Task, BountyGoal

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'bounty']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class BountyGoalForm(forms.ModelForm):
    week_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    
    class Meta:
        model = BountyGoal
        fields = ['week_start_date', 'goal_amount']