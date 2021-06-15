#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Franz Heinzl
#
# save this file as /storage/.kodi/userdata/PWM_fan/PWM_fan.py
#
# Based on:
# https://forum.libreelec.tv/thread/9472-cooling-fan-control-raspberry-pi-libreelec/
# https://hackernoon.com/how-to-control-a-fan-to-cool-the-cpu-of-your-raspberrypi-3313b6e7f92c 
#
# Hardware setup:
# NPN-Transistor: 2N3904
# Emitter connected to GND
# Base connected to GPIO 12 (PWM0) with a 1kOhm resistor in between
# Collector connector to fan and fan connected to 5V
# Pull-Down 10kOhm resistor between GND and GPIO 12
# Diode between Collector and 5V (optional to protect transistor from fan)
#
# Install Libreelec Raspberry Pi Tools addon (Addons --> install from repository --> LibreELEC Add-ons --> Program Addons --> Raspberry PiTools)
# chmod 777 he PWM_fan.py script
#
# PWM_fan.service file needs to go in /storage/.config/system.d
# enable it with "systemctl enable PWM_fan" and start it with "systemctl start PWM_fan"
# check if its working with "systemctl status PWM_fan.service

import os
import time
import signal
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
import RPi.GPIO as GPIO

# Configuration
FAN_PIN = 12  # BCM pin used to drive transistor's base
WAIT_TIME = 5  # [s] Time to wait between each refresh
FAN_MIN = 35  # [%] Fan minimum speed.
PWM_FREQ = 25  # [Hz] Change this value if fan has strange behavior

# Configurable temperature and fan speed steps
# tempSteps = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75]  # [°C]
# speedSteps = [0, 35, 45, 50, 55, 60, 70, 80, 90, 100]  # [%]
# tempSteps = [50, 55, 60, 65, 70, 75, 80]  # [°C]
# speedSteps = [0, 35, 40, 50, 60, 75, 100]  # [%]

# Fan speed will change only of the difference of temperature is higher than hysteresis
hyst = 1

# Setup GPIO pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setwarnings(False)
fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
fan.start(0)

i = 0
cpuTemp = 0
fanSpeed = 0
cpuTempOld = 0
fanSpeedOld = 0

# We must set a speed value for each temperature step
if len(speedSteps) != len(tempSteps):
    print("Numbers of temp steps and speed steps are different")
    exit(0)

try:
    while 1:
        # Read CPU temperature
        cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
        cpuTemp = float(cpuTempFile.read()) / 1000
        cpuTempFile.close()

        # Calculate desired fan speed
        if abs(cpuTemp - cpuTempOld) > hyst:
            # Below first value, fan will run at min speed.
            if cpuTemp < tempSteps[0]:
                fanSpeed = speedSteps[0]
            # Above last value, fan will run at max speed
            elif cpuTemp >= tempSteps[len(tempSteps) - 1]:
                fanSpeed = speedSteps[len(tempSteps) - 1]
            # If temperature is between 2 steps, fan speed is calculated by linear interpolation
            else:
                for i in range(0, len(tempSteps) - 1):
                    if (cpuTemp >= tempSteps[i]) and (cpuTemp < tempSteps[i + 1]):
                        fanSpeed = round((speedSteps[i + 1] - speedSteps[i])
                                         / (tempSteps[i + 1] - tempSteps[i])
                                         * (cpuTemp - tempSteps[i])
                                         + speedSteps[i], 1)

            if fanSpeed != fanSpeedOld:
                if (fanSpeed != fanSpeedOld
                        and (fanSpeed >= FAN_MIN or fanSpeed == 0)):
                    fan.ChangeDutyCycle(fanSpeed)
                    fanSpeedOld = fanSpeed
            cpuTempOld = cpuTemp
            
        # print("temperature: " + str(cpuTemp) + "     fan speed: " + str(fanSpeed))
            
        # Wait until next refresh
        time.sleep(WAIT_TIME)


# If a keyboard interrupt occurs (ctrl + c), the GPIO is set to 0 and the program exits.
except KeyboardInterrupt:
    print("Fan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()
