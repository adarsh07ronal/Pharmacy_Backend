from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='japan') # need to run only once to download and load model into memory
img_path = 'drug1.jpg'
result = ocr.ocr(img_path, cls=True)
if result:
	for i in range(0,len(result)):
		print(result[i][1])
