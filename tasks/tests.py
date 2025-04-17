from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Task, BountyGoal
from .forms import TaskForm, BountyGoalForm

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
    def test_task_creation(self):
        """Test task creation and default values"""
        task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.priority, 'medium')
        self.assertEqual(task.status, 'not_started')
        self.assertEqual(task.bounty, 10)
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.completed_at)
        
    def test_mark_completed(self):
        """Test the mark_completed method"""
        task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )
        
        self.assertEqual(task.status, 'not_started')
        self.assertIsNone(task.completed_at)
        
        task.mark_completed()
        
        self.assertEqual(task.status, 'completed')
        self.assertIsNotNone(task.completed_at)
        
        # Calling mark_completed again should not change the completed_at timestamp
        original_completed_at = task.completed_at
        task.mark_completed()
        self.assertEqual(task.completed_at, original_completed_at)


class BountyGoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
    def test_bounty_goal_creation(self):
        """Test bounty goal creation"""
        today = timezone.now().date()
        goal = BountyGoal.objects.create(
            user=self.user,
            week_start_date=today,
            goal_amount=100
        )
        
        self.assertEqual(goal.user, self.user)
        self.assertEqual(goal.week_start_date, today)
        self.assertEqual(goal.goal_amount, 100)
        
    def test_unique_together_constraint(self):
        """Test that a user cannot have multiple goals for the same week"""
        today = timezone.now().date()
        BountyGoal.objects.create(
            user=self.user,
            week_start_date=today,
            goal_amount=100
        )
        
        # Creating another goal for the same week should fail
        with self.assertRaises(Exception):
            BountyGoal.objects.create(
                user=self.user,
                week_start_date=today,
                goal_amount=200
            )


class TaskFormTest(TestCase):
    def test_valid_task_form(self):
        """Test that the task form validates correctly with valid data"""
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'high',
            'status': 'not_started',
            'bounty': 20
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_task_form(self):
        """Test form validation with invalid data"""
        # Missing required title
        form_data = {
            'description': 'This is a test task',
            'priority': 'high',
            'status': 'not_started',
            'bounty': 20
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        
        # Invalid priority value
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'invalid_priority',
            'status': 'not_started',
            'bounty': 20
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('priority', form.errors)


class BountyGoalFormTest(TestCase):
    def test_valid_bounty_goal_form(self):
        """Test that the bounty goal form validates correctly with valid data"""
        form_data = {
            'week_start_date': timezone.now().date(),
            'goal_amount': 100
        }
        form = BountyGoalForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_bounty_goal_form(self):
        """Test form validation with invalid data"""
        # Missing required goal_amount
        form_data = {
            'week_start_date': timezone.now().date(),
        }
        form = BountyGoalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('goal_amount', form.errors)


class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.task1 = Task.objects.create(
            user=self.user,
            title='Test Task 1',
            priority='high',
            bounty=20
        )
        
        self.task2 = Task.objects.create(
            user=self.user,
            title='Test Task 2',
            status='in_progress',
            bounty=30
        )
        
        self.login_url = reverse('login')
        self.task_list_url = reverse('task_list')
        self.task_create_url = reverse('task_create')
        self.task_update_url = reverse('task_update', args=[self.task1.id])
        self.task_delete_url = reverse('task_delete', args=[self.task1.id])
        self.task_complete_url = reverse('task_complete', args=[self.task1.id])
        self.bounty_dashboard_url = reverse('bounty_dashboard')
        
    def test_login_required(self):
        """Test that views redirect to login page for unauthenticated users"""
        response = self.client.get(self.task_list_url)
        # Our middleware redirects to login without the next parameter
        self.assertRedirects(response, self.login_url)
        
        response = self.client.get(self.task_create_url)
        # Our middleware redirects to login without the next parameter
        self.assertRedirects(response, self.login_url)
        
    def test_task_list_view(self):
        """Test the task list view shows user's tasks"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.task_list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')
        
    def test_task_list_filter(self):
        """Test that the task list can be filtered"""
        self.client.login(username='testuser', password='testpassword123')
        
        # Filter by status
        response = self.client.get(f'{self.task_list_url}?status=in_progress')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 2')
        self.assertNotContains(response, 'Test Task 1')
        
        # Filter by priority
        response = self.client.get(f'{self.task_list_url}?priority=high')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')
        
    def test_task_create_view(self):
        """Test task creation"""
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        
        task_data = {
            'title': 'New Test Task',
            'description': 'A new task for testing',
            'priority': 'medium',
            'status': 'not_started',
            'bounty': 15
        }
        
        response = self.client.post(self.task_create_url, task_data)
        self.assertRedirects(response, self.task_list_url)
        
        # Verify task was created
        self.assertTrue(Task.objects.filter(title='New Test Task').exists())
        
    def test_task_update_view(self):
        """Test task updating"""
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.get(self.task_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        
        updated_data = {
            'title': 'Updated Test Task',
            'description': 'This task has been updated',
            'priority': 'low',
            'status': 'in_progress',
            'bounty': 25
        }
        
        response = self.client.post(self.task_update_url, updated_data)
        self.assertRedirects(response, self.task_list_url)
        
        # Verify task was updated
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.title, 'Updated Test Task')
        self.assertEqual(task.priority, 'low')
        self.assertEqual(task.status, 'in_progress')
        
    def test_task_delete_view(self):
        """Test task deletion"""
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.get(self.task_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')
        
        response = self.client.post(self.task_delete_url)
        self.assertRedirects(response, self.task_list_url)
        
        # Verify task was deleted
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())
        
    def test_task_complete_view(self):
        """Test marking a task as complete"""
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.get(self.task_complete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_complete.html')
        
        response = self.client.post(self.task_complete_url)
        self.assertRedirects(response, self.task_list_url)
        
        # Verify task was marked as completed
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.status, 'completed')
        self.assertIsNotNone(task.completed_at)
        
    def test_bounty_dashboard_view(self):
        """Test the bounty dashboard view"""
        self.client.login(username='testuser', password='testpassword123')
        
        # Create a completed task for testing
        completed_task = Task.objects.create(
            user=self.user,
            title='Completed Task',
            status='completed',
            completed_at=timezone.now(),
            bounty=50
        )
        
        response = self.client.get(self.bounty_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/bounty_dashboard.html')
        
        # Test creating a weekly goal
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        goal_data = {
            'week_start_date': start_of_week.date(),
            'goal_amount': 100
        }
        
        response = self.client.post(self.bounty_dashboard_url, goal_data)
        self.assertRedirects(response, self.bounty_dashboard_url)
        
        # Verify goal was created
        self.assertTrue(BountyGoal.objects.filter(user=self.user, goal_amount=100).exists())
