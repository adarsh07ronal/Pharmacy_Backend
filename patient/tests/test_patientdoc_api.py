import email
from email.policy import HTTP
from os import stat
from urllib import response
from patient.models import Patient, Address, PatientDocument
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
import mock
from django.core.files import File
from django.test import Client

file_mock = mock.MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'

User = get_user_model()

class PatientDocAPITest(APITestCase):
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
        docdata = {
            "employee":patient, 
            "name":"DocTest",
            "date":"2022-01-13",
            "text":"TestingText",
        }
        patientdoc = PatientDocument(**docdata)
        patientdoc.save()


    def test_patientdoc_get(self):
        response = self.client.get("/api/patient_document_api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_patientdoc_post(self):
        docdata = {
            "employee":1,
            "name":"UpdateCheck",
            "date":"2022-01-13",
            "text":"TestingText",
            "created_at":"2022-01-13",
            "file":(open("patient/document/Circles.png","rb"))
        }

        response = self.client.post("/api/patient_document_api/", data=docdata, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PatientDocAPITest2(APITestCase):
    def setUp(self) -> None:
        user = User(id=1,email="shreyans2@eoraa.com",password="Shreyans2!")
        user.save()
        patientdata = {
        "id":2,
        "name": "Shreyans2",
        "nickname": "Shre",
        "dob": "2022-01-13",
        "phone_no": "9999999999",
        "email": "shreyans2@eoraaa.com",
        "gender": "Male",
        "allergy_info": "None",
        "allergy_reactive": "None",
        "type": 1,
        "user": user
        }
        patient = Patient(**patientdata)
        patient.save()
        docdata = {
            "id":1,
            "employee":patient,
            "name":"DocTest",
            "date":"2022-01-13",
            "text":"TestingText",
        }
        patientdoc = PatientDocument(**docdata)
        patientdoc.save()



    def test_patientdoc_get_id(self):
        response = self.client.get("/api/patient_document_api/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_patientdoc_get_invalid_id(self):
        response = self.client.get("/api/patient_document_api/5/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_patientdoc_patch_id(self):
        docdata = {
            "name":"UpdateCheck",
        }
        response = self.client.patch("/api/patient_document_api/1/", data=docdata, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_patientdoc_put_id(self):
        docdata = {
            "employee":2,
            "name":"UpdateCheck",
            "date":"2022-01-13",
            "text":"TestingText",
            "created_at":"2022-01-13",
            "file":(open("patient/document/Circles.png","rb"))
        }
        response = self.client.put("/api/patient_document_api/1/", data=docdata, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    