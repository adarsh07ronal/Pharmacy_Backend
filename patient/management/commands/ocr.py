from django.core.management.base import BaseCommand, CommandError

import cv2
import pytesseract

class Command(BaseCommand):

	def handle(self, *args, **options):
		img = cv2.imread('patient/document/00015.jpg')
		h, w, c = img.shape
		boxes = pytesseract.image_to_boxes(img,'jpn') 
		str = ''
		for b in boxes.splitlines():
		    b = b.split(' ')
		    img1 = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
		    str = str +  b[0]

		print(str)
		img = cv2.resize(img, (960, 540))