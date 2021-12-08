# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 LED 작동시킴

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 100) 

#센서에 연결한 Trig와 Echo 핀의 핀 번호 설정 
TRIG = 23
ECHO = 24
print("Distance measurement in progress")

#Trig와 Echo 핀의 출력/입력 설정 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#Trig핀의 신호를 0으로 출력 
GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)
dis_result = "0cm"

def ultra():
    try:
         
        global dis_result
        GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
        time.sleep(0.00001)       # 10µs 딜레이 
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            start = time.time()	 # Echo 핀 상승 시간 
        while GPIO.input(ECHO)==1:
            stop= time.time()	 # Echo 핀 하강 시간 
            
        check_time = stop - start
        distance = check_time * 34300 / 2
        dis_result = distance+"cm"
        print("Distance : %.1f cm" % distance)
            
        time.sleep(0.4)	# 0.4초 간격으로 센서 측정 
                        
            
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/dis/on")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def ultra():
    try:
        while True:
            global dis_result

            GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
            time.sleep(0.00001)       # 10µs 딜레이 
            GPIO.output(TRIG, False)
            
            while GPIO.input(ECHO)==0:
                start = time.time()	 # Echo 핀 상승 시간 
            while GPIO.input(ECHO)==1:
                stop= time.time()	 # Echo 핀 하강 시간 
                
            check_time = stop - start
            distance = check_time * 34300 / 2
            dis_result = distance+"cm"
            print("Distance : %.1f cm" % distance)
                
            time.sleep(0.4)	# 0.4초 간격으로 센서 측정 

            return dis_result                         # 함수가 'ok'문자열을 반환함
    except :
        return "fail"



if __name__ == "__main__":
    app.run(host="0.0.0.0")
