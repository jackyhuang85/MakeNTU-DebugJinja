face_api_url = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0/detect'
headers = {'Ocp-Apim-Subscription-Key': '',
           'Content-Type': 'application/octet-stream'
           }

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}
