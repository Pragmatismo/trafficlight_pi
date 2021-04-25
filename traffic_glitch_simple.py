#!/usr/bin/python3
import os
import sys
import time
import datetime
import random
import threading
homedir = os.getenv("HOME")
os.chdir(homedir + "/trafficlight_pi/")
mode = "pwm" # set to true to show command line output rather than use the GPIO
if mode == "gpio":
    import RPi.GPIO as GPIO

    # Pin Numbers
    gpio_green = 7
    gpio_amber = 8
    gpio_red   = 25

    #initial board setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(gpio_green, GPIO.OUT)
    GPIO.setup(gpio_amber, GPIO.OUT)
    GPIO.setup(gpio_red, GPIO.OUT)

elif mode == "pwm":
    from board import SCL, SDA
    import busio
     # Import the PCA9685 module.
    from adafruit_pca9685 import PCA9685
    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)
    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)
    # Set the PWM frequency to 60hz.
    pca.frequency = 60


# load from file
def load_from_file(load_location, key_to_use):
    timing_list = []
    # Load file
    with open(load_location, "r") as f:
        file_text = f.read()
    # cycle through each line
    file_text = file_text.splitlines()
    for line in file_text:
        if not line.strip()[:1] == "#":
            name, key, data = line.split(">")
            data = data.split(",")
            # create list of timings
            data_list = []
            prior_time = 0
            for item in data:
                item = item.split("=")
                #print (item)
                if len(item) == 2:
                    timing_item = float(item[1]) - prior_time
                    prior_time = float(item[1])
                    data_list = data_list + [ [ item[0], timing_item ] ]
            if key in key_to_use:
                timing_list.append(data_list)
                print(" Loaded " + key + " (" + name + ") " + str(len(data_list)))
    return timing_list

def load_lamp_conf(conf_file):
    '''
    Load's the lamp config file which lays out which lights to use and which cycles to use with them

    format -
         red=file=filename_red:abc,on=5
         <light colour>=<type on/off/file>=<duration>
                                           <file_name:letter channel>
    '''
    with open(conf_file, "r") as f:
        file_text = f.read()
    file_text = file_text.splitlines()
    # Read light
    lamp_dict = {}
    lamps_to_use = []
    for line in file_text:
        line = line.strip()
        equals_pos = line.find("=")
        colour = line[:equals_pos]
        lamps_to_use.append(colour)
        action_string = line[equals_pos+1:].split(",")
        lamp_action_list = []
        for action in action_string:
            action = action.split("=")
            if action[0] == "file":
                filename = action[1].split(":")[0]
                keys = action[1].split(":")[1]
                #print("Loading keys - " + keys + " from " + filename)
                file_timings = load_from_file(filename, keys)
                action = ["file", file_timings]
            lamp_action_list.append(action)
        lamp_dict[colour] = lamp_action_list
    return lamps_to_use, lamp_dict


def text_light(colour, duration, timing_list):
    #time_now = time.time()
    #while time.time() < time_now + duration:
    for x in timing_list:
        direction = x[0]
        flicker_time = float(x[1])
        if flicker_time < 0:
            flicker_time = 0
        #print(direction + " " + str(flicker_time))
        if direction == "D":
            light_on(colour)
            time.sleep(flicker_time)
        else:
            light_off(colour)
            time.sleep(flicker_time)

pwm_channels = {"green":1, "amber":2, "red":0}

# lamp control functions
def light_on(colour):
    if mode == "gpio":
        if colour == "green":
            GPIO.output(gpio_green, GPIO.LOW)
        elif colour == "amber":
            GPIO.output(gpio_amber, GPIO.LOW)
        elif colour == "red":
            GPIO.output(gpio_red, GPIO.LOW)
    elif mode == "pwm":
        pca.channels[pwm_channels[colour]].duty_cycle = 0xffff
    else:
        print("  + Turning on " + colour)

def light_off(colour):
    if mode == 'gpio':
        if colour == "green":
            GPIO.output(gpio_green, GPIO.HIGH)
        elif colour == "amber":
            GPIO.output(gpio_amber, GPIO.HIGH)
        elif colour == "red":
            GPIO.output(gpio_red, GPIO.HIGH)
    elif mode == "pwm":
        pca.channels[pwm_channels[colour]].duty_cycle = 0
    else:
        print("  - Turning off " + colour)

# patterns
def flicker_light(colour, duration, shortest_flicker, longest_flicker):
    time_now = time.time()
    while time.time() < time_now + float(duration):
        flicker_time = random.uniform(shortest_flicker, longest_flicker)
        light_on(colour)
        if flicker_time < 0:
            flicker_time = 0
        time.sleep(flicker_time)
        light_off(colour)
        flicker_time = random.uniform(shortest_flicker, longest_flicker)
        if flicker_time < 0:
            flicker_time = 0
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


def light_trigger(lamp, mode, duration):
    if mode == "on":
        #print(lamp + " LIGHT ON")
        light_on(lamp)
        time.sleep(float(duration))
    if mode == "off":
        #print(lamp + " LIGHT off")
        light_off(lamp)
        time.sleep(float(duration))
    if mode == "flicker":
        shortest_flicker = 0.1
        longest_flicker = 1
        flicker_light(lamp, duration, shortest_flicker, longest_flicker)
    if mode == "percent":
        flicker_time = 0.1
        flickers = [5, 10, 25, 50, 75, 90, 95]
        p_light(lamp, duration, flicker_time, flickers)
    if mode == "file":
        timing_lists = duration
        list_choice = random.randint(0, len(timing_lists)-1)
        #print(len(timing_lists), " lists, using ", list_choice)
        text_light(lamp, "0", timing_lists[list_choice])

# light pattern loop
if __name__ == '__main__':
    # initial state
    r_cycle = 0
    a_cycle = 0
    g_cycle = 0
    lights_to_use, lamp_dict = load_lamp_conf('test_conf.txt')

    if "red" in lights_to_use:
        red_cycle = lamp_dict['red']
        red_thread = threading.Thread(target=red_light, args=("on",5,))#, daemon=True)
        red_thread.start()
        red_start = datetime.datetime.now()
    if "amber" in lights_to_use:
        amber_cycle = lamp_dict['amber']
        amber_thread = threading.Thread(target=amber_light, args=("on",2,))#, daemon=True)
        amber_thread.start()
    if "green" in lights_to_use:
        green_cycle = lamp_dict['green']
        green_thread = threading.Thread(target=green_light, args=(green_cycle[g_cycle][0],green_cycle[g_cycle][1]))
        green_thread.start()
    # Start the loop
    while True:
        # Red Thread
        if "red" in lights_to_use:
            if not red_thread.is_alive():
                time_since_start = datetime.datetime.now() - red_start
                print(time_since_start)
                time_since_start = datetime.datetime.now()
                r_cycle = r_cycle + 1
                if r_cycle > len(red_cycle)-1:
                    r_cycle = 0
                red_thread = threading.Thread(target=red_light, args=(red_cycle[r_cycle][0],red_cycle[r_cycle][1]))
                red_thread.start()
        # Amber Thread
        if "amber" in lights_to_use:
            if not amber_thread.is_alive():
                a_cycle = a_cycle + 1
                if a_cycle > len(amber_cycle)-1:
                    a_cycle = 0
                amber_thread = threading.Thread(target=amber_light, args=(amber_cycle[a_cycle][0],amber_cycle[a_cycle][1]))
                amber_thread.start()
        # Green Thread
        if "green" in lights_to_use:
            if not green_thread.is_alive():
                g_cycle = g_cycle + 1
                if g_cycle > len(green_cycle)-1:
                    g_cycle = 0
                green_thread = threading.Thread(target=green_light, args=(green_cycle[g_cycle][0],green_cycle[g_cycle][1]))
                green_thread.start()
