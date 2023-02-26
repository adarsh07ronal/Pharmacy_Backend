import email
from patient.models import Patient, Address, PatientDocument
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientAPITest(APITestCase):
    def setUp(self):
        user = User(id=1,email="shreyans@eoraa.com",password="Shreyans1!")
        user.save()
    
    def test_patient_post(self):
        data = {
        "name": "Shreyans",
        "nickname": "Shre",
        "dob": "2022-01-13",
        "phone_no": "9999999999",
        "email": "shreyans@eoraa.com",
        "gender": "Male",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": 1
        }
        response = self.client.post("/api/patient_api/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_get(self):
        response = self.client.get("/api/patient_api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_noemail(self):
        data = {
        "name": "Shreyans",
        "nickname": "Shre",
        "dob": "2022-01-13",
        "phone_no": "9999999999",
        "gender": "Male",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": 1
        }
        response = self.client.post("/api/patient_api/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_noname(self):
        data = {
        "nickname": "Shre",
        "dob": "2022-01-13",
        "phone_no": "9999999999",
        "email": "shreyans@eoraa.com",
        "gender": "Male",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": 1
        }
        response = self.client.post("/api/patient_api/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_nodob(self):
        data = {
        "name": "Shreyans",
        "nickname": "Shre",
        "phone_no": "9999999999",
        "email": "shreyans@eoraa.com",
        "gender": "Male",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": 1
        }
        response = self.client.post("/api/patient_api/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_nogender(self):
        data = {
        "name": "Shreyans",
        "nickname": "Shre",
        "phone_no": "9999999999",
        "dob": "2022-01-13",
        "email": "shreyans@eoraa.com",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": 1
        }
        response = self.client.post("/api/patient_api/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        

class PatientAPITestwithID(APITestCase):
    def setUp(self) -> None:
        user = User(id=1,email="shreyans@eoraa.com",password="Shreyans1!")
        user.save()
        data = {
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
        patient = Patient(**data)
        patient.save()

    def test_patient_get_id(self):
        response = self.client.get("/api/patient_api/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patient_put_id(self):
        data = {
        "name": "UpdateCheck",
        "nickname": "Shre",
        "dob": "2022-01-13",
        "phone_no": "9999999999",
        "email": "shreyans@eoraa.com",
        "gender": "Male",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": 1
        }
        response = self.client.put("/api/patient_api/1/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patient_patch_id(self):
        data = {
        "name": "UpdateCheck",
        }
        response = self.client.patch("/api/patient_api/1/", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_delete_id(self):
        response = self.client.delete("/api/patient_api/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




