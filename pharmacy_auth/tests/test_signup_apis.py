from rest_framework import status
from rest_framework.test import APITestCase


class OrthrusAuthAPITest(APITestCase):
    url="/api/orthrus/signup/"

    def setUp(self):
        data={"email":"shreyans_exists@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
    
    def test_signup_nopassword(self):
        data={"email":"shreyans@eoraa.com","password":""}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_signup_noemail(self):
        data={"email":"","password":"shreyans"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_signup_invalidpassword_nospecial(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_signup_invalidpassword_noalpha(self):
        data={"email":"shreyans@eoraa.com","password":"123456!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_signup_invalidpassword_nodigit(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_signup(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_alreadyexists(self):
        data={"email":"shreyans_exists@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PatientAuthAPITest(APITestCase):
    url="/api/patient/signup/"

    def setUp(self):
        data={"email":"shreyans_exists@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')

    def test_signup_nopassword(self):
        data={"email":"shreyans@eoraa.com","password":""}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_noemail(self):
        data={"email":"","password":"shreyans"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nospecial(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_noalpha(self):
        data={"email":"shreyans@eoraa.com","password":"123456!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nodigit(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_alreadyexists(self):
        data={"email":"shreyans_exists@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class PharmacyAuthAPITest(APITestCase):
    url="/api/pharmacy/signup/"

    def setUp(self):
        data={"email":"shreyans_exists@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')

    def test_signup_nopassword(self):
        data={"email":"shreyans@eoraa.com","password":""}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_noemail(self):
        data={"email":"","password":"shreyans"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nospecial(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_noalpha(self):
        data={"email":"shreyans@eoraa.com","password":"123456!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidpassword_nodigit(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans!"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup(self):
        data={"email":"shreyans@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_alreadyexists(self):
        data={"email":"shreyans_exists@eoraa.com","password":"Shreyans!1"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

