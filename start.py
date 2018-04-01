# Make NTU Group 15 - More happier when playing together
from importlib import import_module
import cv2
import requests
import json
import RPi.GPIO as GPIO
from time import sleep
from config import face_api_url, params, headers


def capture(cam):
    ret, frame = cam.read()
    ret, frame = cam.read()
    ret, frame = cam.read()
    cv2.imwrite('face.jpg', frame)


def judge_face():
    img_data = None
    with open('face.jpg', 'rb') as f:
        img_data = f.read()

    try:
        response = requests.post(face_api_url, params=params,
                                 headers=headers, data=img_data,
                                 timeout=10)
                                 
        faces = response.json()
        # print(faces)
        if faces != []:
            emotion = faces[0]["faceAttributes"]["emotion"]
            print(emotion)
            return emotion
        return None
    except requests.exceptions.RequestException:
        print('Timeout, recapture img')
    except Exception as e:
        print(e)
        return None


def setAngle(pwm, pin, angle):
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)


def worship(num):
    pwm = GPIO.PWM(3, 50)
    pwm.start(0)
    while num > 0:
        setAngle(pwm, 3, 90)
        setAngle(pwm, 3, 0)
        num -= 1
    pwm.stop()


def wave_flag(num):
    pwm = GPIO.PWM(7, 50)
    pwm.start(0)
    while num > 0:
        setAngle(pwm, 7, 180)
        setAngle(pwm, 7, 0)
        num -= 1
    pwm.stop()


def decide_motion(emotion):
    bad = ['anger', 'contempt', 'disgust', 'sadness', 'fear']
    good = ['happiness', 'surprise']
    
    bad_score = 0
    for key in bad:
        bad_score += emotion[key]
    good_score = 0
    for key in good:
        good_score += emotion[key]

    if emotion['neutral'] > 0.9:
        pass
    elif bad_score * 10 > good_score:
        GPIO.output(5, GPIO.HIGH)
        worship(6)
    else:
        wave_flag(5)


if __name__ == "__main__":
    print('Start program')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    cam = cv2.VideoCapture(0)
    while True:
        GPIO.output(5, GPIO.LOW)
        capture(cam)
        print('img captured')
        emotion = judge_face()
        if emotion is not None:
            decide_motion(emotion)
        sleep(1)

    GPIO.cleanup()
