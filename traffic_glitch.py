#!/usr/bin/python3
import time
import random
import threading
import RPi.GPIO as GPIO

# Pin Numbers
gpio_green = 7
gpio_amber = 8
gpio_red   = 25
gpio_walk  = 24
gpio_dontwalk = 23
gpio_wait = 18

initial board setup
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

#testing
# def light_on(colour):
#     print(" ON - " + colour)
#
# def light_off(colour):
#     print(" OFF - " + colour)

def flicker_light(colour, duration, shortest_flicker, longest_flicker):
    time_now = time.time()
    while time.time() < time_now + duration:
        flicker_time = random.uniform(shortest_flicker, longest_flicker)
        light_on(colour)
        time.sleep(flicker_time)
        light_off(colour)
        flicker_time = random.uniform(shortest_flicker, longest_flicker)
        time.sleep(flicker_time)


def p_light(colour, duration, flicker_time, flickers):
    '''
    This takes a list of percentage positions and flickers the light at each one,
    a list of [10,50,90] with a duration of ten seconds would flash the lights
    after one second, five seconds and nine seconds.
    '''
    time_now = time.time()
    duration_percent = float(duration) / 100
    prior = 0.0
    for x in flickers:
        off_wait = (float(x) - prior) * (duration_percent)
        prior = x
        sleep_time = off_wait - flicker_time
        if sleep_time < 0:
            sleep_time = 0
        time.sleep(sleep_time)
        #print("----f----", x, " :", off_wait, " : ", time.time() - time_now)
        light_on(colour)
        time.sleep(flicker_time)
        light_off(colour)

def red_light(mode, duration):
    light_trigger("red", mode, duration)

def amber_light(mode, duration):
    light_trigger("amber", mode, duration)

def green_light(mode, duration):
    light_trigger("green", mode, duration)

def walk_light(mode, duration):
    light_trigger("walk", mode, duration)

def dontwalk_light(mode, duration):
    light_trigger("dontwalk", mode, duration)

def wait_light(mode, duration):
    light_trigger("wait", mode, duration)

def light_trigger(lamp, mode, duration):
    if mode == "on":
        #print(lamp + " LIGHT ON")
        light_on(lamp)
        time.sleep(duration)
    if mode == "off":
        #print(lamp + " LIGHT off")
        light_off(lamp)
        time.sleep(duration)
    if mode == "flicker":
        shortest_flicker = 0.1
        longest_flicker = 1
        flicker_light(lamp, duration, shortest_flicker, longest_flicker)
    if mode == "percent":
        flicker_time = 0.1
        flickers = [5, 10, 25, 50, 75, 90, 95]
        p_light(lamp, duration, flicker_time, flickers)

red_cycle = [["on", 0.5], ["off", 0.1], ["percent", 5], ["off", 2]]
amber_cycle = [["on", 10], ["flicker", 10]]
green_cycle = [["flicker", 3], ["off", 6], ["on", 3]]
walk_cycle = [["off", 5], ["on", 5]]
dontwalk_cycle = [["on", 5], ["off", 5]]
wait_cycle = [["on", 3], ["off", 4]]


# light pattern loop
if __name__ == '__main__':
    # initial state
    r_cycle = 0
    a_cycle = 0
    g_cycle = 0
    w_cycle = 0
    dw_cycle = 0
    wt_cycle = 0
    red_thread = threading.Thread(target=red_light, args=("on",5,))#, daemon=True)
    amber_thread = threading.Thread(target=amber_light, args=("on",2,))#, daemon=True)
    green_thread = threading.Thread(target=green_light, args=(green_cycle[g_cycle][0],green_cycle[g_cycle][1]))
    walk_thread = threading.Thread(target=walk_light, args=(walk_cycle[g_cycle][0],walk_cycle[g_cycle][1]))
    dontwalk_thread = threading.Thread(target=dontwalk_light, args=(dontwalk_cycle[dw_cycle][0],dontwalk_cycle[dw_cycle][1]))
    wait_thread = threading.Thread(target=wait_light, args=(wait_cycle[wt_cycle][0],wait_cycle[wt_cycle][1]))
    red_thread.start()
    amber_thread.start()
    green_thread.start()
    walk_thread.start()
    dontwalk_thread.start()
    wait_thread.start()
    while True:
        # Red Thread
        if not red_thread.is_alive():
            r_cycle = r_cycle + 1
            if r_cycle > len(red_cycle)-1:
                r_cycle = 0
            red_thread = threading.Thread(target=red_light, args=(red_cycle[r_cycle][0],red_cycle[r_cycle][1]))
            red_thread.start()
        # Amber Thread
        if not amber_thread.is_alive():
            a_cycle = a_cycle + 1
            if a_cycle > len(amber_cycle)-1:
                a_cycle = 0
            amber_thread = threading.Thread(target=amber_light, args=(amber_cycle[a_cycle][0],amber_cycle[a_cycle][1]))
            amber_thread.start()
        # Green Thread
        if not green_thread.is_alive():
            g_cycle = g_cycle + 1
            if g_cycle > len(green_cycle)-1:
                g_cycle = 0
            green_thread = threading.Thread(target=green_light, args=(green_cycle[g_cycle][0],green_cycle[g_cycle][1]))
            green_thread.start()
        # walk thread
        if not walk_thread.is_alive():
            w_cycle = w_cycle + 1
            if w_cycle > len(walk_cycle)-1:
                w_cycle = 0
            walk_thread = threading.Thread(target=walk_light, args=(walk_cycle[w_cycle][0],walk_cycle[w_cycle][1]))
            walk_thread.start()
        # dontwalk thread
        if not dontwalk_thread.is_alive():
            dw_cycle = dw_cycle + 1
            if dw_cycle > len(dontwalk_cycle)-1:
                dw_cycle = 0
            dontwalk_thread = threading.Thread(target=dontwalk_light, args=(dontwalk_cycle[dw_cycle][0],dontwalk_cycle[dw_cycle][1]))
            dontwalk_thread.start()
        # wait thread
        if not wait_thread.is_alive():
            wt_cycle = wt_cycle + 1
            if wt_cycle > len(wait_cycle)-1:
                wt_cycle = 0
            wait_thread = threading.Thread(target=wait_light, args=(wait_cycle[wt_cycle][0],wait_cycle[wt_cycle][1]))
            wait_thread.start()
