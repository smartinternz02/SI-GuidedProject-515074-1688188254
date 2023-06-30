from flask import Flask,render_template,Response, url_for, redirect, request
import cv2
import mediapipe as mp
import numpy as np
from keras.models import  load_model
from tensorflow.keras.utils import img_to_array 
from tensorflow.keras.preprocessing import image


app=Flask(__name__)
cap = ""


def detect_hand(hand_landmarks, frame):
    height, width, _ = frame.shape
    landmarks_x = [landmark.x * width for landmark in hand_landmarks.landmark]
    landmarks_y = [landmark.y * height for landmark in hand_landmarks.landmark]
    x_min = int(min(landmarks_x))-20
    x_max = int(max(landmarks_x))+20
    y_min = int(min(landmarks_y))-20
    y_max = int(max(landmarks_y))+20

    if x_min != -1 and y_min != -1:
        hand_width = x_max - x_min
        hand_height = y_max - y_min

        # Calculate the center of the hand bounding box
        center_x = x_min + hand_width // 2
        center_y = y_min + hand_height // 2

        # Calculate the starting and ending coordinates for the 224x224 region
        crop_size = 224
        crop_start_x = center_x - crop_size // 2
        crop_start_y = center_y - crop_size // 2
        crop_end_x = crop_start_x + crop_size
        crop_end_y = crop_start_y + crop_size

        # Ensure the cropping region is within the frame boundaries
        crop_start_x = max(crop_start_x, 0)
        crop_start_y = max(crop_start_y, 0)
        crop_end_x = min(crop_end_x, width)
        crop_end_y = min(crop_end_y, height)

    # Check if the crop coordinates are within the frame boundaries
    if x_min < 0 or x_max > width or y_min < 0 or y_max > height:
        return -1, -1, -1, -1  # Invalid crop coordinates

    return crop_start_x, crop_start_y, crop_end_x, crop_end_y


def generate_frames():
    global cap
    cap = cv2.VideoCapture(0)
    
    
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    mp_drawing_styles = mp.solutions.drawing_styles

    # Loading the pre-trained MediaPipe hand detection model
    hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1, min_detection_confidence=0.3)   

    model = load_model('model.h5')
        
    while True:
        while True:
            ret, frame = cap.read()

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform hand detection
            results = hands.process(frame_rgb)

            # If hand is detected, crop and save the image
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]

                # Get bounding box coordinates of the hand
                x_min, y_min, x_max, y_max = detect_hand(hand_landmarks, frame)

                # If the bounding box is valid, crop and save the image
                if x_min != -1 and y_min != -1:
                    cropped_image = frame[y_min:y_max, x_min:x_max]
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                                  mp_drawing_styles.get_default_hand_landmarks_style(),
                                                  mp_drawing_styles.get_default_hand_connections_style())
                    img1 = cv2.resize(cropped_image, (224, 224),
                                      interpolation=cv2.INTER_AREA)
                    img1 = image.img_to_array(img1)
                    img1 = np.expand_dims(img1, axis=0)
                    pred = np.argmax(model.predict(img1))

                    output = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K',
                              'L', 'O', 'P', 'Q', 'R', 'S', 'U', 'V', 'W', 'X', 'Y']

                    cv2.putText(frame, str(
                        output[pred]), (x_min, y_min-10), cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
                    if x_min != -1 and y_min != -1:
                        cv2.rectangle(frame, (x_min, y_min),
                                      (x_max, y_max), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/Start')
def Start():
    global cap
    if cap != "":
        cap.release()
    return render_template('homepage.html')

@app.route('/Sign')
def Sign():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

## Emotion Detection
@app.route('/emotion')
def emotion():
    return render_template('index2.html')

@app.route('/form', methods=['POST'])
def upload_file():
    if 'imageFile' in request.files:
        image_file = request.files['imageFile']
        file_name = image_file.filename
        print(f"Uploaded file name: {file_name}")
        img_path = "./static/css/image_emotion/" + file_name
        image_file.save(img_path)
    else:
        print("No file uploaded")

    test_img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    #Loading the model
    model = load_model("emotion_det.h5")

    #Detecting face from the image
    face_haar_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
    print("Faces: ", faces_detected)

    if len(faces_detected) == 0:  # If no face detected
        roi_gray = cv2.resize(gray_img, (48, 48))
        img_pixels = img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255
        predictions = model.predict(img_pixels)

        # find max indexed array
        max_index = np.argmax(predictions[0])

        emotions = ('Anger', 'Disgust', 'Fear', 'Happy',
                    'Neutral', 'Sadness', "Surprise")
        predicted_emotion = emotions[max_index]
        resized_img = cv2.resize(test_img, (1000, 700))

    else:  # If face has been detected
        print("Face outline Detected")
        for (x, y, w, h) in faces_detected:
            print("Hello")
            print(test_img.shape)
            cv2.rectangle(test_img, (x, y), (x + w, y + h),
                          (255, 0, 0), thickness=7)
            # cropping region of interest i.e. face area from  image
            roi_gray = gray_img[y:y + w, x:x + h]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            img_pixels = img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255

            predictions = model.predict(img_pixels)

            # find max indexed array
            max_index = np.argmax(predictions[0])

            emotions = ('Anger', 'Disgust', 'Fear', 'Happy',
                        'Neutral', 'Sadness', "Surprise")
            predicted_emotion = emotions[max_index]

            #Calculate coordinates of a point from the original image in the resized image
            def calculate_resized_coordinates(original_width, original_height, resized_width, resized_height, point):
                # Calculate the ratio of width and height
                width_ratio = resized_width / original_width
                height_ratio = resized_height / original_height

                # Calculate the corresponding coordinates in the resized image
                resized_x = int(point[0] * width_ratio)
                resized_y = int(point[1] * height_ratio)

                return resized_x, resized_y

            resized_img = cv2.resize(test_img, (1000, 700))
            print((test_img.shape[1], test_img.shape[0],
                  1000, 700, (int(x), int(y))))
            x1, y1 = calculate_resized_coordinates(
                test_img.shape[1], test_img.shape[0], 1000, 700, (int(x), int(y)))
            cv2.putText(resized_img, predicted_emotion, (int(x1), int(
                y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # resized_img = cv2.resize(test_img, (1000, 700))
    #cv2.imshow('Facial emotion analysis ', resized_img)
    cv2.imwrite(
        './static/css/image_emotion/' + file_name, resized_img)
    print("Prediction: ", predicted_emotion)
    return render_template("index3.html", img_src=file_name, pred=predicted_emotion)

@app.route('/back')
def back():
    return render_template('index2.html')

if __name__=="__main__":
    app.run()
