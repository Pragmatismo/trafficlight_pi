#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

# Pin Numbers
gpio_green = 7
gpio_amber = 8
gpio_red   = 25
gpio_walk  = 24

# initial board setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpio_green, GPIO.OUT)
GPIO.setup(gpio_amber, GPIO.OUT)
GPIO.setup(gpio_red, GPIO.OUT)
GPIO.setup(gpio_walk, GPIO.OUT)

# lamp control functions
def light_on(colour):
    print("  + Turning on " + colour)
    if colour == "green":
        GPIO.output(gpio_green, GPIO.HIGH)
    elif colour == "amber":
        GPIO.output(gpio_amber, GPIO.HIGH)
    elif colour == "red":
        GPIO.output(gpio_red, GPIO.HIGH)
    elif colour == "walk":
        GPIO.output(gpio_walk, GPIO.HIGH)

def light_off(colour):
    print("  - Turning off " + colour)
    if colour == "green":
        GPIO.output(gpio_green, GPIO.LOW)
    elif colour == "amber":
        GPIO.output(gpio_amber, GPIO.LOW)
    elif colour == "red":
        GPIO.output(gpio_red, GPIO.LOW)
    elif colour == "walk":
        GPIO.output(gpio_walk, GPIO.LOW)

# light pattern loop
if __name__ == '__main__':
    # initial state
    print("Starting traffic light loop")
    light_on("green")
    light_off("red")
    light_off("amber")
    # loop
    while true:
        time.sleep(15)
        light_off("green")
        light_on("amber")
        time.sleep(15)
        light_off("amber")
        light_on("red")
        time.sleep(15)
        light_on("amber")
        time.sleep(15)
        light_off("red")
        light_off("amber")
        light_on("green")
