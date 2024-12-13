from django.test import TestCase
from .models import User, UserProfile, ECard
from django.utils import timezone
from cryptography.fernet import Fernet

class UserProfileModelTest(TestCase):

    def setUp(self):
        # Set up a test user
        self.user = User.objects.create(username="testuser")
        self.profile = UserProfile.objects.create(
            user=self.user,
            aadhaar="123456789012",
            pan="ABCDE1234F",
            mobile_number="9876543210",
            bank_details="Bank XYZ, Account No: 1234567890"
        )

    def test_user_profile_creation(self):
        # Test the creation of the UserProfile
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.aadhaar, "123456789012")
        self.assertEqual(self.profile.pan, "ABCDE1234F")
        self.assertEqual(self.profile.mobile_number, "9876543210")
        self.assertEqual(self.profile.bank_details, "Bank XYZ, Account No: 1234567890")

    def test_encrypt_data(self):
        # Test encryption of sensitive data
        self.profile.encrypt_data()
        self.assertNotEqual(self.profile.aadhaar, "123456789012")  # The data should be encrypted
        self.assertNotEqual(self.profile.pan, "ABCDE1234F")
        self.assertNotEqual(self.profile.mobile_number, "9876543210")
        self.assertNotEqual(self.profile.bank_details, "Bank XYZ, Account No: 1234567890")

    def test_decrypt_data(self):
        # Test decryption of sensitive data
        self.profile.encrypt_data()
        self.profile.decrypt_data()
        self.assertEqual(self.profile.aadhaar, "123456789012")
        self.assertEqual(self.profile.pan, "ABCDE1234F")
        self.assertEqual(self.profile.mobile_number, "9876543210")
        self.assertEqual(self.profile.bank_details, "Bank XYZ, Account No: 1234567890")


class ECardModelTest(TestCase):

    def setUp(self):
        # Set up a test user and profile
        self.user = User.objects.create(username="testuser")
        self.profile = UserProfile.objects.create(
            user=self.user,
            aadhaar="123456789012",
            pan="ABCDE1234F",
            mobile_number="9876543210",
            bank_details="Bank XYZ, Account No: 1234567890"
        )
        self.ecard = ECard.objects.create(user=self.user, card_data="Some card data")

    def test_ecard_creation(self):
        # Test ECard creation and its fields
        self.assertEqual(self.ecard.user.username, "testuser")
        self.assertEqual(self.ecard.card_data, "Some card data")

    def test_generate_card(self):
        # Test card generation logic
        generated_card = self.ecard.generate_card()
        self.assertIn("Virtual E-Card for 123456789012", generated_card)


class AdminActionsTest(TestCase):

    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create(username="testuser")
        self.profile = UserProfile.objects.create(
            user=self.user,
            aadhaar="123456789012",
            pan="ABCDE1234F",
            mobile_number="9876543210",
            bank_details="Bank XYZ, Account No: 1234567890"
        )
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpassword")
        self.client.login(username="admin", password="adminpassword")

    def test_approve_user_action(self):
        # Test the approve action on UserProfile admin
        response = self.client.post('/admin/ecard/userprofile/', {
            "_selected_action": [str(self.profile.id)],  # Selecting the profile to approve
            "action": "approve_user"
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.status, "Approved")
        self.assertTrue(self.profile.ecard_generated)

    def test_reject_user_action(self):
        # Test the reject action on UserProfile admin
        response = self.client.post('/admin/ecard/userprofile/', {
            "_selected_action": [str(self.profile.id)],  # Selecting the profile to reject
            "action": "reject_user"
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.status, "Rejected")
        self.assertFalse(self.profile.ecard_generated)

