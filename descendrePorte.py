import RPi.GPIO as GPIO
import time
import socket
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
PIN_BUTTON_BAS=17
PIN_BUTTON_HAUT=27
duty=5.35
go=True

def get_lock(process_name):
    global lock_socket   # Without this our lock gets garbage collected
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + process_name)
        print 'I got the lock'
    except socket.error:
        print 'lock exists'
        sys.exit(0)


def system_button(PIN_BUTTON):
 duty=7.0
 pwm.ChangeDutyCycle(duty)
 #pwm.stop()
 #GPIO.cleanup()
 #quit()


def main():
 if (GPIO.input(PIN_BUTTON_BAS) == False): # le bouton est presse...
  quit()
 pwm.start(5.5)
 go=True
 ncount=0
 while go:
  time.sleep(0.5)
  if (GPIO.input(PIN_BUTTON_BAS) == False) or ncount>40 or (GPIO.input(PIN_BUTTON_HAUT)==False): # le bouton est presse...
     go=False
  ncount=ncount+1
 pwm.stop()
 print 'stop descend'


if __name__ == "__main__":
    get_lock('porte')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_BUTTON_HAUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_BUTTON_BAS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PIN_BUTTON_BAS, GPIO.FALLING, callback=system_button, bouncetime=200)
    try:
     main()
    finally: 
     GPIO.cleanup()
     lock_socket.close()
