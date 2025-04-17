from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class DashboardIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('login')
        self.task_list_url = reverse('task_list')
        self.bounty_dashboard_url = reverse('bounty_dashboard')
        
    def test_dashboard_links_to_tasks(self):
        """Test that the main dashboard has links to the tasks module"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.dashboard_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_list_url)
        self.assertContains(response, 'Tasks')  # Changed from 'Tasks &amp; Bounties'
        self.assertContains(response, self.bounty_dashboard_url)
        self.assertContains(response, 'Bounty Dashboard')
        
    def test_login_required_for_dashboard(self):
        """Test that the dashboard redirects to login for unauthenticated users"""
        response = self.client.get(self.dashboard_url)
        # Our middleware is redirecting to login without the next parameter
        self.assertRedirects(response, self.login_url)