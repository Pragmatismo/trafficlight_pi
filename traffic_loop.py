#!/usr/bin/python3
import time
import random
import RPi.GPIO as GPIO

# Pin Numbers
gpio_green = 7
gpio_amber = 8
gpio_red   = 25
gpio_walk  = 24
gpio_dontwalk = 23
gpio_wait = 18

# initial board setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpio_green, GPIO.OUT)
GPIO.setup(gpio_amber, GPIO.OUT)
GPIO.setup(gpio_red, GPIO.OUT)
GPIO.setup(gpio_walk, GPIO.OUT)
GPIO.setup(gpio_dontwalk, GPIO.OUT)
GPIO.setup(gpio_wait, GPIO.OUT)

# lamp control functions
def light_on(colour):
    print("  + Turning on " + colour)
    if colour == "green":
        GPIO.output(gpio_green, GPIO.LOW)
    elif colour == "amber":
        GPIO.output(gpio_amber, GPIO.LOW)
    elif colour == "red":
        GPIO.output(gpio_red, GPIO.LOW)
    elif colour == "walk":
        GPIO.output(gpio_walk, GPIO.LOW)
    elif colour == "dontwalk":
        GPIO.output(gpio_dontwalk, GPIO.LOW)
    elif colour == "wait":
        GPIO.output(gpio_wait, GPIO.LOW)

def light_off(colour):
    print("  - Turning off " + colour)
    if colour == "green":
        GPIO.output(gpio_green, GPIO.HIGH)
    elif colour == "amber":
        GPIO.output(gpio_amber, GPIO.HIGH)
    elif colour == "red":
        GPIO.output(gpio_red, GPIO.HIGH)
    elif colour == "walk":
        GPIO.output(gpio_walk, GPIO.HIGH)
    elif colour == "dontwalk":
        GPIO.output(gpio_dontwalk, GPIO.HIGH)
    elif colour == "wait":
        GPIO.output(gpio_wait, GPIO.HIGH)

def flicker_light(colour, duration, shortest_flicker, longest_flicker):
    time_now = time.time()
    while time.time() < time_now + duration:
        flicker_time = random.uniform(shortest_flicker, longest_flicker)
        light_on(colour)
        time.sleep(flicker_time)
        light_off(colour)
        flicker_time = random.uniform(shortest_flicker, longest_flicker)
        time.sleep(flicker_time)

# light pattern loop
if __name__ == '__main__':
    # initial state
    print("Starting traffic light loop")
    light_off("amber")
    light_off("red")
    light_off("dontwalk")
    light_off("wait")
    light_on("green")
    light_on("walk")
    # loop
    while True:
        print("")
        time.sleep(15)
        flicker_light("green", 15, 0.001, 1)
        light_off("walk")
        light_on("amber")
        light_on("dontwalk")
        light_on("wait")
        time.sleep(15)
        light_off("amber")
        flicker_light("red", 15, 0.01, 2)
        time.sleep(15)
        flicker_light("red", 15, 0.1, 0.5)
        light_on("amber")
        time.sleep(15)
        light_off("red")
        light_off("amber")
        light_off("dontwalk")
        light_off("wait")
        light_on("green")
        light_on("walk")
