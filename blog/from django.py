from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_landing_view(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')

    def test_landing_login_view(self):
        response = self.client.get(reverse('landingLogin'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('landing'))

        response = self.client.post(reverse('landingLogin'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account'))

    def test_login_user_view(self):
        response = self.client.get(reverse('loginUser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_register.html')

        response = self.client.post(reverse('loginUser'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account'))

    def test_logout_user_view(self):
        response = self.client.get(reverse('logoutUser'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_register_user_view(self):
        response = self.client.get(reverse('registerUser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_register.html')

        response = self.client.post(reverse('registerUser'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit-account'))

    def test_edit_account_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('editAccount'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_form.html')

        response = self.client.post(reverse('editAccount'), {
            'field1': 'value1',
            'field2': 'value2'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('landing'))

    def test_edit_account_view_unauthenticated(self):
        response = self.client.get(reverse('editAccount'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_edit_account_view_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('editAccount'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_form.html')

    def tearDown(self):
        self.profile.delete()
        self.user.delete()
