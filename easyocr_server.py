from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np
from matplotlib import pyplot as plt

THRESHOLD = 0.5

app = Flask(__name__)
reader = easyocr.Reader(['ko', 'en'])

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img_array = np.fromstring(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    result = reader.readtext(img)
    response = []

    for bbox, text, conf in result:
        if conf > THRESHOLD:
            response.append({'text': text, 'confidence': conf})

            # bbox 좌표를 int로 변환하여 사용
            pt1 = (int(bbox[0][0]), int(bbox[0][1]))
            pt2 = (int(bbox[2][0]), int(bbox[2][1]))
            cv2.rectangle(img, pt1=pt1, pt2=pt2, color=(0, 255, 0), thickness=3)

    # 결과 확인을 위해 이미지 표시 (원하는 경우 주석 해제)
    # plt.figure(figsize=(8, 8))
    # plt.imshow(img[:, :, ::-1])
    # plt.axis('off')
    # plt.show()

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5555)
