import subprocess
import os
import sys
import struct
import bluetooth._bluetooth as bluez
import bluetooth
import thread
import subprocess
import time
import re
import RPi.GPIO as GPIO
from twilio.rest import TwilioRestClient

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
umbrella_on = True
twilio_on =True
get_byte = ord
distance = -1000
rain = True
lightsOn = False

def byte_to_signed_int(byte_):
    if byte_>127:
        return byte_ - 256
    else:
        return byte_

def listenBT():
    global twilio_on, umbrella_on

    while True:
        server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        server_sock.bind(("",bluetooth.PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        bluetooth.advertise_service( server_sock, "SampleServer",
                        service_id = uuid,
                        service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                        profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
                            )

        print("Waiting for connection on RFCOMM channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        try:
            while True:
                data = client_sock.recv(1024)
                if len(data) == 0: break
                if data == "hey tamayo":
                        client_sock.send("holaaa")
                if data == "umbrella_off":
                        umbrella_on = False
                if data == "umbrella_on":
                        umbrella_on = True
                if data == "twilio_on":
                        twilio_on = True                 
		if data == "twilio_off":                         
			twilio_on = False
                print("received [%s]" % data)
        except IOError:
            pass

        print("disconnected")

        client_sock.close()
        server_sock.close()
        print("all done")
#	account_sid = "xxxxx"
#	auth_token  = "xxxxx"
#	client = TwilioRestClient(account_sid, auth_token)
#	call = client.calls.create(url="https://gist.githubusercontent.com/dtd93/d374f962aeede7f947e7a2c5880cd19c/raw/b6e2daef2370209deef6bfa759c4e2387eaacad8/gistfile1.txt", to="xxxx",from_="xxxx")
#	print(call.sid)
	if twilio_on and umbrella_on:
		subprocess.call("./scriptCall.sh")	

def toggleLightsOn():
    lightsOn = True
    GPIO.output(8,True) ## Turn on GPIO pin 7
    GPIO.output(10,True) ## Turn on GPIO pin 7
    GPIO.output(12,True) ## Turn on GPIO pin 7
    GPIO.output(16,True) ## Turn on GPIO pin 7
    GPIO.output(18,True) ## Turn on GPIO pin 7
    GPIO.output(22,True) ## Turn on GPIO pin 7
    GPIO.output(24,True) ## Turn on GPIO pin 7
    GPIO.output(26,True) ## Turn on GPIO pin 7
    GPIO.output(40,True) ## Turn on GPIO pin 7

def toggleLightsOff():
    lightsOn = False
    GPIO.output(8,False) ## Turn on GPIO pin 7
    GPIO.output(10,False) ## Turn on GPIO pin 7
    GPIO.output(12,False) ## Turn on GPIO pin 7
    GPIO.output(16,False) ## Turn on GPIO pin 7
    GPIO.output(18,False) ## Turn on GPIO pin 7
    GPIO.output(22,False) ## Turn on GPIO pin 7
    GPIO.output(24,False) ## Turn on GPIO pin 7
    GPIO.output(26,False) ## Turn on GPIO pin 7
    GPIO.output(40,False) ## Turn on GPIO pin 7

def checkDistance():
    while True:
        res = subprocess.Popen('hcitool rssi "78:00:9E:32:7D:37"', shell=True, stdout=subprocess.PIPE).stdout.read()

        p = re.compile('RSSI return value: (.*)')
        resArr = p.findall(res)

        if len(resArr) > 0:
            distance = int(resArr[0])

            if distance > -15 and rain == True and lightsOn == False and umbrella_on:
                toggleLightsOn()
            elif not rain or distance <= -15 or not umbrella_on:
                toggleLightsOff()

        time.sleep(1)

thread.start_new_thread(listenBT, ())
thread.start_new_thread(checkDistance, ())

while True:
    continue
