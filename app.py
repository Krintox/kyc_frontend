import cv2 as cv
import easyocr
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importing CORS
import base64

app = Flask(__name__)

# Setting up CORS for specified origins
CORS(app, resources={r"/verify_details": {"origins": ["http://localhost:3000", "http://127.0.0.1:5000", "https://kycauto.com"]}})

reader = easyocr.Reader(['en'])

# Helper function to decode base64 image
def get_img(base64_image):
    im_bytes = base64.b64decode(base64_image)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
    return img

# Detect and encode faces using OpenCV
def get_face_encodings(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]
    face_region = img[y:y + h, x:x + w]
    return face_region

# Compare two faces based on structural similarity (simple pixel comparison)
def same_person(img1, img2, threshold=0.5):
    face_encodings1 = get_face_encodings(img1)
    face_encodings2 = get_face_encodings(img2)

    if face_encodings1 is None or face_encodings2 is None:
        return False

    # Resize faces for comparison
    face1_resized = cv.resize(face_encodings1, (100, 100))
    face2_resized = cv.resize(face_encodings2, (100, 100))

    difference = cv.absdiff(face1_resized, face2_resized)
    similarity_score = np.sum(difference) / (100 * 100 * 255)

    return similarity_score < threshold

@app.route('/verify_details', methods=['POST'])
def verify_details():
    form = request.json
    name = form["name"].upper().replace(" ", "")
    dob = form["dob"]
    idType = form["idType"]
    idNum = form["idNum"].replace(" ", "")
    idImage = get_img(form["idFront"])
    selfie = get_img(form["selfie"])

    # OCR Processing
    text = reader.readtext(idImage)
    concatenated_text = ''.join([detection[1].replace(' ', '').upper() for detection in text])

    # Verification
    authenticated = 0
    description = ''
    if name not in concatenated_text:
        authenticated = 1
        description += 'Name not matched \n'
    if dob not in concatenated_text:
        authenticated = 1
        description += 'DOB not matched \n'
    if idNum not in concatenated_text:
        authenticated = 1
        description += f'{idType} number not matched \n'
    
    # Face Verification
    if authenticated == 0:
        face_match = same_person(idImage, selfie)
        if not face_match:
            authenticated = 2
            description += 'Face not matched \n'
    
    if authenticated == 0:
        description = f'{idType} verified successfully'
    
    result = {
        'result': authenticated,
        'description': description
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
