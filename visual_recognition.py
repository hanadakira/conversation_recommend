import json
from watson_developer_cloud import VisualRecognitionV3
import cv2
from PIL import Image, ImageDraw, ImageFilter

visual_recognition = VisualRecognitionV3(
    '2018-12-09',
    iam_apikey='DmEtTvXslo8CUhKYF9EK9WzZW8_D7tOTHAG1wkOj4naS')

with open('prez.jpg', 'rb') as images_file:
    faces = visual_recognition.detect_faces(images_file).get_result()
#print(json.dumps(faces, indent=2))
#human_info = json.dumps(faces, indent=2)
#print(human_info[0])
info = faces["images"][0]["faces"]
face_location = info[0]["face_location"]    #顔の位置情報を取得

img = cv2.imread("prez.jpg", 1)
cap = cv2.imread("cap1.jpg", 1)
cap = cv2.resize(cap, (face_location["height"], face_location["width"]))    #帽子のサイズを顔のサイズにリサイズ
cv2.imwrite("cap2.jpg", cap)

cv2.rectangle(img, (face_location["left"], face_location["top"]), (face_location["left"] + face_location["width"], face_location["top"] + face_location["height"]), (0, 0, 255), 5) #顔の位置に矩形を描画
cv2.imwrite("comp.jpg", img)

im1 = Image.open('comp.jpg')
im2 = Image.open('cap2.jpg')

back_im = im1.copy()
back_im.paste(im2, (face_location["left"], face_location["top"]-face_location["height"]))
back_im.save('gousei.jpg', quality=95)