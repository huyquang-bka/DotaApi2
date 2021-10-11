import cv2
import time
import easyocr

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
reader = easyocr.Reader(['ch_sim','en'], gpu=True) # this needs to run only once to load the model into memory
start = time.time()
img = cv2.imread("roshan_hp.png")
img_hp_current = img[1022: 1022 + 18, 843 : 843 + 71]

result = reader.readtext(img_hp_current, detail=0)
# text_current = pytesseract.image_to_string(img_hp_current,
#                                            config='--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789',
#                                            lang="eng")
#
print(result)
print(time.time() - start)

# cv2.imshow("gray_hp_current", img_hp_current)
# cv2.waitKey()
