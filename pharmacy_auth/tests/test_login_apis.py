from rest_framework.test import APITestCase
from rest_framework import status

class PatientAuthAPITest(APITestCase):
    url='/api/login/'

    def setUp(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!1"}
        response = self.client.post("/api/patient/signup/", data=data, format='json')

    def test_login(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalidcreds(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans2!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nopassword(self):
        data={"email":"shreyans_patient@eoraa.com","password":""}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_noemail(self):
        data={"email":"","password":"shreyans"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nospecial(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_noalpha(self):
        data={"email":"shreyans_patient@eoraa.com","password":"123456!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nodigit(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrthrusAuthAPITest(APITestCase):
    url='/api/login/'

    def setUp(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!1"}
        response = self.client.post("/api/orthrus/signup/", data=data, format='json')

    def test_login(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalidcreds(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans2!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nopassword(self):
        data={"email":"shreyans_patient@eoraa.com","password":""}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_noemail(self):
        data={"email":"","password":"shreyans"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nospecial(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_noalpha(self):
        data={"email":"shreyans_patient@eoraa.com","password":"123456!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nodigit(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PharmacyAuthAPITest(APITestCase):
    url='/api/login/'

    def setUp(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!1"}
        response = self.client.post("/api/pharmacy/signup/", data=data, format='json')

    def test_login(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalidcreds(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans2!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nopassword(self):
        data={"email":"shreyans_patient@eoraa.com","password":""}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_noemail(self):
        data={"email":"","password":"shreyans"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nospecial(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_noalpha(self):
        data={"email":"shreyans_patient@eoraa.com","password":"123456!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nodigit(self):
        data={"email":"shreyans_patient@eoraa.com","password":"Shreyans!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)