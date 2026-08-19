from django.test import TestCase, Client
from django.urls import reverse
from charityapp.models import login_table, detail_table, Contact
from charityapp.services import AuthService, ContextService

class CharityAuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user with hashed password
        self.user = AuthService.register_user(
            name="Test User",
            email="testuser@example.com",
            password="securepassword123",
            phone=9876543210,
            role="User"
        )
        # Create a legacy user with plain-text password for backward compatibility testing
        self.legacy_user = login_table.objects.create(
            name="Legacy User",
            email="legacyuser@example.com",
            password="legacypassword",
            phone_no=1234567890,
            role="User",
            status="1"
        )

    def test_auth_service_hashed_password(self):
        authenticated_user = AuthService.authenticate_user("testuser@example.com", "securepassword123")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.email, "testuser@example.com")

    def test_auth_service_legacy_password_upgrade(self):
        # Authenticate legacy user
        authenticated_user = AuthService.authenticate_user("legacyuser@example.com", "legacypassword")
        self.assertIsNotNone(authenticated_user)
        # Verify that the password was automatically upgraded to hashed format
        self.assertNotEqual(authenticated_user.password, "legacypassword")

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_contact_submission(self):
        response = self.client.post(reverse('submitcontact'), {
            'name': 'Test Donor',
            'email': 'donor@example.com',
            'subject': 'Help Inquiry',
            'message': 'I want to donate books.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(email='donor@example.com').exists())
