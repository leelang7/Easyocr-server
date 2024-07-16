import requests

def upload_image(image_path):
    url = 'http://localhost:5555/upload'
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print('Text detection successful. Here are the results:')
        for item in response.json():
            print(f"Text: {item['text']} - Confidence: {item['confidence']}")
    else:
        print(f"Failed to upload image. Server response code: {response.status_code}")

if __name__ == '__main__':
    image_path = '01.jpg'
    upload_image(image_path)
