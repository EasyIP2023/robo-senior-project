import RPi.GPIO as GPIO
import Robot

GPIO.setmode(GPIO.BOARD)

RIGHT_WHEEL_PIN = 32
LEFT_WHEEL_PIN = 33

#Set up input pins for encoders
GPIO.setup(RIGHT_WHEEL_PIN, GPIO.IN, GPIO.PUD_UP) #right wheel
GPIO.setup(LEFT_WHEEL_PIN, GPIO.IN, GPIO.PUD_UP) #left wheel

#optimized for 5 inches; moving more or less than that will 
#result in a larger margin of error
def goDistanceLeft(distance):
	distSoFar = 0
	initPosition = GPIO.input(LEFT_WHEEL_PIN)
	while (distSoFar < distance):
		while(GPIO.input(LEFT_WHEEL_PIN) == 1):
			pass
		distSoFar += 0.35  #distance (in inches) with each slot rotation of encoder
		while(GPIO.input(LEFT_WHEEL_PIN) == 0):
			pass
	return 1
	
def goDistanceRight(distance):
	distSoFar = 0
	initPosition = GPIO.input(RIGHT_WHEEL_PIN)
	while (distSoFar < distance):
		while(GPIO.input(RIGHT_WHEEL_PIN) == initPosition):
			pass
		distSoFar += 0.35 #distance (in inches) with each slot rotation of encoder
		while(GPIO.input(RIGHT_WHEEL_PIN) != initPosition):
			pass
	return 1		



robot = Robot.Robot()

robot.forward(127)
goDistanceLeft(5.00)
robot.stop()
