import unittest

from flask_login import current_user
from flask_testing import TestCase

from app.models.user import User
from app.views import user_accounts, app

user_accounts.create_user(User("Fellow1", "fellow1@andela.com", "bootcampertofellow"))


class BaseTestCase(TestCase):
    ''' A base test case. '''

    # Creating an instance of our flask app
    def create_app(self):
        app.config.from_object('app.instance.config.TestingConfig')
        return app


class FlaskTestCase(BaseTestCase):
    # Test that flask was set up correctly
    # Test client is what we use to create a test mocking functionality of a current app
    def test_index(self):
        response = self.client.get('/', content_type="html/text")
        self.assertEqual(response.status_code, 200)

    # Test that the dashboard route is protected
    def test_dashboard_route_is_protected_and_requires_login(self):
        response = self.client.get('/api/v1/auth/dashboard', follow_redirects=True)
        self.assertTrue(b'Please Login First to access this page' in response.data)


class UserViewsTests(BaseTestCase):
    # Test that login page loads correctly
    def test_login_page_loads_correctly(self):
        response = self.client.get('/', content_type="html/text")
        self.assertTrue(b'Login' in response.data)

    # Test that the login page behaves correctly given correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post('/', data=dict(username="Fellow1", password="bootcampertofellow"),
                                        follow_redirects=True)
            self.assertIn(b'Welcome', response.data)
            self.assertTrue(current_user.id == 'Fellow1')

    # Test login behaves correctly given the incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post('/', data=dict(username="Fellow1", password="felixwambiri@gmail.com"),
                                    follow_redirects=True)
        self.assertTrue(b'Invalid credentials' in response.data)

    # Test logout behaves correctly
    # But first we need to login
    def test_logout(self):
        with self.client:
            self.client.post('/', data=dict(username="Fellow1", password="bootcampertofellow"),
                             follow_redirects=True)
            response = self.client.get('/api/v1/auth/logout', follow_redirects=True)
            self.assertIn(b'You are logged out', response.data)

    # Ensure that the logout route requires user first to be logged in to use it
    def test_logout_route_requires_user_to_be_logged_in(self):
        response = self.client.get('/api/v1/auth/logout', follow_redirects=True)
        self.assertTrue(b'Please Login First to access this page' in response.data)

    # Ensure that user can register
    def test_user_registration(self):
        with self.client:
            response = self.client.post('/api/v1/auth/register',
                                        data=dict(username="quagmire", email="quagmire@gmail.com",
                                                  password="lois&peter&meg",
                                                  confirm_password="lois&peter&meg"),
                                        follow_redirects=True)
            self.assertIn(b'You have been registered successfully and can proceed to login', response.data)

    # Ensure id is correct for the current/logged in user
    def test_get_correct_id(self):
        with self.client:
            self.client.post('/', data=dict(username="Fellow1", password="bootcampertofellow"),
                             follow_redirects=True)
            self.assertTrue(current_user.id == 'Fellow1')

    # Test that a user can create an event
    def test_user_can_create_an_event(self):
        with self.client:
            self.client.post('/', data=dict(username="Fellow1", password="bootcampertofellow"),
                             follow_redirects=True)
            response = self.client.post('/api/v1/events',
                                        data=dict(name="Blaze", category="Learning", location="Nairobi", owner="Andela",
                                                  description="It is a long established fact that a reader will "
                                                              "be distracted by the readable content of a page when "
                                                              "looking at its layout. The point of using Lorem Ipsum "
                                                              "is that it has a more-or-less normal distribution "),
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Dashboard', response.data)


if __name__ == '__main__':
    unittest.main()
