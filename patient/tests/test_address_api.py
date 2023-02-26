from urllib import response
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from patient.models import Address, Patient
from rest_framework import status

User = get_user_model()

class AddressAPITest(APITestCase):
    def setUp(self) -> None:
        user = User(id=1,email="shreyans@eoraa.com",password="Shreyans1!")
        user.save()
        patientdata = {
        "id":1,
        "name": "Shreyans",
        "nickname": "Shre",
        "dob": "2022-01-13",
        "phone_no": "9999999999",
        "email": "shreyans@eoraa.com",
        "gender": "Male",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": user
        }
        patient = Patient(**patientdata)
        patient.save()
        addressdata = {
        "id":2,
        "full_address": "Test Address",
        "city": "Delhi",
        "county": "India",
        "zipcode": "110001",
        "telephone": "9988776655",
        "patient": patient
        }
        address = Address(**addressdata)
        address.save()

    def test_address_get(self):
        response = self.client.get('/api/address_api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_post(self):
        data = {
        "full_address": "New Address for POST",
        "city": "Kanpur",
        "county": "India",
        "zipcode": "208022",
        "telephone": "9876543210",
        "patient": 1
        }
        response = self.client.post('/api/address_api/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_address_post_invalid(self):
        data = {
        "city": "Kanpur",
        "county": "India",
        "zipcode": "208022",
        "telephone": "9876543210",
        "patient": 1
        }
        response = self.client.post('/api/address_api/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_address_get_id(self):
        response = self.client.get('/api/address_api/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_get_id_invalid(self):
        response = self.client.get('/api/address_api/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_address_put_id(self):
        data = {
        "full_address": "New Address for POST",
        "city": "Kanpur",
        "county": "India",
        "zipcode": "208022",
        "telephone": "9876543210",
        "patient": 1
        }
        response = self.client.put('/api/address_api/2/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_patch_id(self):
        data = {
        "full_address": "New Address",
        }
        response = self.client.patch('/api/address_api/2/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_patch_id_2(self):
        data = {
        "city": "Delhi",
        "county": "Malaysia",
        }
        response = self.client.patch('/api/address_api/2/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_delete_id(self):
        response = self.client.delete('/api/address_api/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
