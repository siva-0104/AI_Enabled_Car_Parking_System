import cv2
import pickle
import cvzone as cz
import numpy as np

slot_width, slot_height = 107, 48

try:
    with open(r'C:\Users\siva\Downloads\CarParkingOpenCV\CarParkingOpenCV\ModelBuilding\parkingSlotPosition', 'rb') as file:
        parking_slots = pickle.load(file)
except FileNotFoundError:
    parking_slots = []

def handle_mouse_events(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        parking_slots.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(parking_slots):
            x1, y1 = poscle
            if x1 < x < x1 + slot_width and y1 < y < y1 + slot_height:
                parking_slots.pop(i)

    with open(r'C:\Users\siva\Downloads\CarParkingOpenCV\CarParkingOpenCV\ModelBuilding\parkingSlotPosition', 'wb') as file:
        pickle.dump(parking_slots, file)

while True:
    img = cv2.imread(r'C:\Users\siva\Downloads\CarParkingOpenCV\CarParkingOpenCV\ModelBuilding\carParkImg.png')
    for pos in parking_slots:
        cv2.rectangle(img, pos, (pos[0] + slot_width, pos[1] + slot_height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", handle_mouse_events)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
