from flask import Flask, render_template, redirect, url_for
import cv2
import pickle
import cvzone as cz
import numpy as np

app = Flask(__name__)

@app.route('/')
def render_project():
    return render_template('index.html')

@app.route('/index.html')
def render_home():
    return render_template('index.html')

@app.route('/model.html')
def render_model():
    return render_template('model.html')

@app.route('/login.html')
def render_login():
    return render_template('login.html')

@app.route('/aboutus.html')
def render_aboutus():
    return render_template('aboutus.html')

@app.route('/signup.html')
def render_signup():
    return render_template('signup.html')

@app.route('/contactus.html')
def render_contactus():
    return render_template('contactus.html')

@app.route('/modelq', methods=['POST'])
def live_prediction():
    video_path = r'C:\Users\siva\Downloads\CarParkingOpenCV\CarParkingOpenCV\flask\uploads\carParkingInput.mp4'
    slot_positions_path = r'C:\Users\siva\Downloads\CarParkingOpenCV\CarParkingOpenCV\flask\uploads\parkingSlotPosition'
    
    cap = cv2.VideoCapture(video_path)
    with open(slot_positions_path, 'rb') as file:
        pos_list = pickle.load(file)
    slot_width, slot_height = 107, 48

    def check_parking_space(processed_img):
        space_counter = 0
        for position in pos_list:
            x, y = position
            img_crop = processed_img[y:y + slot_height, x:x + slot_width]
            count = cv2.countNonZero(img_crop)
            if count < 900:
                color = (0, 255, 0)
                thickness = 5
                space_counter += 1
            else:
                color = (0, 0, 255)
                thickness = 2
            cv2.rectangle(img, position, (position[0] + slot_width, position[1] + slot_height), color, thickness)
        cz.putTextRect(img, f'Free: {space_counter}/{len(pos_list)}', (100, 50), scale=3, thickness=5, offset=20,
                       colorR=(0, 200, 0))

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        if not success:
            break
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                             25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)
        check_parking_space(img_dilate)
        cv2.imshow("Image", img)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return redirect(url_for('model'))

if __name__ == "__main__":
    app.run(debug=True)
