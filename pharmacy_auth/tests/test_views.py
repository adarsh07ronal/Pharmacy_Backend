from django.contrib.auth import get_user_model
from django.test import TestCase, Client

# from pharmacy_auth.tests.auth_objects import get_employee
# from pharmacy_auth.tests.check_methods import check_process_view_post, check_template_and_status_code
# from pharmacy_auth.views import login_view, login_page, logout_view
# from settings.models import Currency

User = get_user_model()


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user_email = "test@something.com"
        self.test_user_password = 'secret123'
        User.objects.create_user(
            email=self.test_user_email,
            password=self.test_user_password
        )
    
    def test_user_model_correctcreds(self):
        user = User.objects.get(email="test@something.com")
        self.assertEqual(user.check_password(self.test_user_password),True)
        self.assertEqual(user.email,self.test_user_email)

    def test_user_model_incorrectcreds_email(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email="test1@something.com")

    def test_user_model_incorrectcreds_password(self):
        user = User.objects.get(email="test@something.com")
        self.assertEqual(user.check_password("abcd1234"),False)

    



    # Test api here  whether view returns the right status code and data
