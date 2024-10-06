import cv2
import pickle
import cvzone as cz
import numpy as np

video_path = r'C:\Users\siva\Downloads\CarParkingOpenCV\CarParkingOpenCV\ModelBuilding\carParkingInput.mp4'
slot_positions_path = r'C:\Users\siva\Downloads\CarParkingOpenCV\CarParkingOpenCV\ModelBuilding\parkingSlotPosition'


slot_width, slot_height = 103, 43

with open(slot_positions_path, 'rb') as file:
    parking_slots = pickle.load(file)

def do_nothing(parameter):
    pass

cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Thresh1", "Settings", 25, 50, do_nothing)
cv2.createTrackbar("Thresh2", "Settings", 16, 50, do_nothing)
cv2.createTrackbar("Thresh3", "Settings", 5, 50, do_nothing)

def count_free_spaces():
    free_spaces = 0
    for position in parking_slots:
        x, y = position
        w, h = slot_width, slot_height

        cropped_img = img_thresh[y:y + h, x:x + w]
        pixel_count = cv2.countNonZero(cropped_img)

        color = (0, 200, 0) if pixel_count < 900 else (0, 0, 200)
        thickness = 5 if pixel_count < 900 else 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)
        cv2.putText(img, str(pixel_count), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

        if pixel_count < 900:
            free_spaces += 1

    cz.putTextRect(img, f'Free: {free_spaces}/{len(parking_slots)}', (50, 60), thickness=3, offset=20,
                   colorR=(0, 200, 0))

cap = cv2.VideoCapture(video_path)

while True:
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)

    thresh1 = cv2.getTrackbarPos("Thresh1", "Settings")
    thresh2 = cv2.getTrackbarPos("Thresh2", "Settings")
    thresh3 = cv2.getTrackbarPos("Thresh3", "Settings")

    thresh1 += 1 if thresh1 % 2 == 0 else 0
    thresh3 += 1 if thresh3 % 2 == 0 else 0

    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, thresh1, thresh2)
    img_thresh = cv2.medianBlur(img_thresh, thresh3)
    kernel = np.ones((3, 3), np.uint8)
    img_thresh = cv2.dilate(img_thresh, kernel, iterations=1)

    count_free_spaces()

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
