#!/usr/bin/python3
import time
import random

mode = "pwm" # set to true to show command line output rather than use the GPIO
if mode == "gpio":
    import RPi.GPIO as GPIO

    # Pin Numbers
    gpio_channels = {"green":7, "amber":8, "red":25, "walk_light":24, "dont_walk":23, "wait_light":18}
    gpio_green = 7
    gpio_amber = 8
    gpio_red   = 25
    gpio_walk  = 24
    gpio_dontwalk = 23
    gpio_wait = 18

    #initial board setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for key, value in gpio_channels.items():
        GPIO.setup(value, GPIO.OUT)
    #GPIO.setup(gpio_green, GPIO.OUT)
    #GPIO.setup(gpio_amber, GPIO.OUT)
    #GPIO.setup(gpio_red, GPIO.OUT)
    #GPIO.setup(gpio_walk, GPIO.OUT)
    #GPIO.setup(gpio_dontwalk, GPIO.OUT)
    #GPIO.setup(gpio_wait, GPIO.OUT)
elif mode == "pwm":
    from board import SCL, SDA
    import busio
    from adafruit_pca9685 import PCA9685
    i2c_bus = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c_bus)
    pca.frequency = 60
    pwm_channels = {"green":1, "amber":2, "red":0, "walk_light":4, "dont_walk":3, "wait_light":5}


# lamp control functions
def light_on(colour):
    if mode == "gpio":
        GPIO.output(gpio_channels[colour], GPIO.LOW)
    #    if colour == "green":
    #        GPIO.output(gpio_green, GPIO.LOW)
    #    elif colour == "amber":
    #        GPIO.output(gpio_amber, GPIO.LOW)
    #    elif colour == "red":
    #        GPIO.output(gpio_red, GPIO.LOW)
    #    elif colour == "walk_light":
    #        GPIO.output(gpio_walk, GPIO.LOW)
    #    elif colour == "dont_walk":
    #        GPIO.output(gpio_dontwalk, GPIO.LOW)
        #elif colour == "wait_light":
        #    GPIO.output(gpio_wait, GPIO.LOW)
    elif mode == "pwm":
        pca.channels[pwm_channels[colour]].duty_cycle = 0xffff
    else:
        print("")
    print("  + Turning on " + colour)

def light_off(colour):
    if mode == 'gpio':
        GPIO.output(gpio_channels[colour], GPIO.HIGH)
    #    if colour == "green":
    #        GPIO.output(gpio_green, GPIO.HIGH)
    #    elif colour == "amber":
    #        GPIO.output(gpio_amber, GPIO.HIGH)
    #    elif colour == "red":
    #        GPIO.output(gpio_red, GPIO.HIGH)
    #    elif colour == "walk_light":
    #        GPIO.output(gpio_walk, GPIO.HIGH)
    #    elif colour == "dont_walk":
    #        GPIO.output(gpio_dontwalk, GPIO.HIGH)
    #    elif colour == "wait_light":
    #        GPIO.output(gpio_wait, GPIO.HIGH)
    elif mode == "pwm":
        pca.channels[pwm_channels[colour]].duty_cycle = 0
    else:
        print(" ")
    print("  - Turning off " + colour)



def time_random(colours, chance, seconds):
    second = 0
    while not second >= seconds:
        for colour in colours:
            dice = random.randint(0, 100)
            if chance > dice:
                light_on(colour)
                colours.remove(colour)
        second = second + 1
        time.sleep(1)

def time_flickers(colours, chance, seconds, shortest_flicker, longest_flicker):
    second = 0
    while not second >= seconds:
        for colour in colours:
            flicker_time = 0
            dice = random.randint(0, 100)
            if chance > dice:
                flicker_time = random.uniform(shortest_flicker, longest_flicker)
                light_on(colour)
                time.sleep(flicker_time)
                light_off(colour)
        second = second + 1
        if flicker_time > 1:
            flicker_time = 1
        time.sleep(1 - flicker_time)


# light pattern loop
if __name__ == '__main__':
    # initial state
    print("Starting traffic light loop")
    light_off("amber")
    light_off("red")
    light_off("dont_walk")
    light_off("wait_light")
    light_on("green")
    light_on("walk_light")
    # loop
    while True:
        print("")
        time.sleep(15)
        light_off("green")
        light_off("walk_light")
        light_on("amber")
        #light_on("dont_walk")
        #light_on("wait")
        time_random(["wait_light", "dont_walk"], 50, 15)
        #time.sleep(15)
        light_off("amber")
        #light_on("red")
        time_flickers(["red"], 20, 5, 0.001, 0.05)
        time_flickers(["red"], 50, 5, 0.1, 0.15)
        time_random(["red"], 50, 5)
        #time.sleep(15)
        #light_on("red")
        time_flickers(["amber"], 20, 5, 0.001, 0.05)
        time_flickers(["amber"], 50, 5, 0.1, 0.15)
        time_random(["amber"], 20, 5)
        #light_on("amber")
        #time.sleep(15)
        light_off("red")
        light_off("amber")
        light_off("dont_walk")
        light_off("wait_light")
        light_on("green")
        light_on("walk_light")
