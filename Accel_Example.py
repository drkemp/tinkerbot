#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import smbus
from MPU6050 import MPU6050

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=True)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

accel = MPU6050()

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def limit(min, max, value) :
  if( value < min ) :
    return min
  elif(value > max ) :
    return max
  else :
    return value

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
cval = 300
while (True):
  cval = limit(150, 600, cval + accel.getAccel(0)/1000)
  # Change speed of continuous servo on channel O
  pwm.setPWM(0, 0, cval)
  time.sleep(1)
  print "temp  =" + repr( accel.getTemp())
  print "X =" + repr( accel.getAccel(0))
  print "Y =" + repr( accel.getAccel(1))
  print "Z =" + repr( accel.getAccel(2))
  print "cval =" + repr( cval)


