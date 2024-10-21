from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewTestCase(TestCase):

    def setUp(self):
        """Create a test client and a sample user."""
        self.client = Client()
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_index_view_redirects_anonymous_user(self):
        """Index view should redirect anonymous users to the login page."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('login'))  # Check redirection target

    def test_index_view_accessible_to_authenticated_user(self):
        """Index view should be accessible to authenticated users."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Should return OK
        self.assertTemplateUsed(response, 'users/index.html')  # Check correct template

    def test_login_view_get(self):
        """Login view should display the login form on GET request."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)  # Should return OK
        self.assertTemplateUsed(response, 'users/login.html')  # Check correct template

    def test_login_view_post_valid_credentials(self):
        """Login view should authenticate and redirect with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('index'))  # Check redirection target

    def test_login_view_post_invalid_credentials(self):
        """Login view should return an error message with invalid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should return OK
        self.assertTemplateUsed(response, 'users/login.html')  # Check correct template
        self.assertContains(response, 'Invalid credentials.')  # Check for error message

    def test_logout_view(self):
        """Logout view should log out the user and display the login page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)  # Should return OK
        self.assertTemplateUsed(response, 'users/login.html')  # Check correct template
        self.assertContains(response, 'Logged out')  # Check for logout message

        # Verify that the user is logged out
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('login'))  # Should redirect to login