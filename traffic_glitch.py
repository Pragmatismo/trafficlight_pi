#!/usr/bin/python3
import sys
import time
import random
import threading
testing = True # set to true to show command line output rather than use the GPIO
if not testing == True:
    import RPi.GPIO as GPIO

    # Pin Numbers
    gpio_green = 7
    gpio_amber = 8
    gpio_red   = 25
    gpio_walk  = 24
    gpio_dontwalk = 23
    gpio_wait = 18

    #initial board setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(gpio_green, GPIO.OUT)
    GPIO.setup(gpio_amber, GPIO.OUT)
    GPIO.setup(gpio_red, GPIO.OUT)
    GPIO.setup(gpio_walk, GPIO.OUT)
    GPIO.setup(gpio_dontwalk, GPIO.OUT)
    GPIO.setup(gpio_wait, GPIO.OUT)

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
                print("Loading keys - " + keys + " from " + filename)
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
        #print(direction + " " + str(flicker_time))
        if direction == "D":
            light_on(colour)
            time.sleep(flicker_time)
        else:
            light_off(colour)
            time.sleep(flicker_time)


# lamp control functions
def light_on(colour):
    if not testing == True:
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
    else:
        print("  + Turning on " + colour)

def light_off(colour):
    if not testing == True:
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
    else:
        print("  - Turning off " + colour)

# patterns
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
        print(len(timing_lists), " lists, using ", list_choice)
        text_light(lamp, "0", timing_lists[list_choice])



#red_cycle = [["on", 0.5], ["off", 0.1], ["percent", 5], ["off", 2]]
#amber_cycle = [["on", 10], ["flicker", 10]]
#green_cycle = [["flicker", 3], ["off", 6], ["on", 3]]
#red_cycle = [["file", 5]]
#amber_cycle = [["on", 5], ["off", 5]]
#green_cycle = [["off", 5], ["on", 5]]
#walk_cycle = [["off", 5], ["on", 5]]
dontwalk_cycle = [["on", 5], ["off", 5]]
wait_cycle = [["on", 3], ["off", 5]]


# light pattern loop
if __name__ == '__main__':
    # initial state
    r_cycle = 0
    a_cycle = 0
    g_cycle = 0
    w_cycle = 0
    dw_cycle = 0
    wt_cycle = 0

    #lights_to_use = ["red", "amber", "green", "walk_light", "dont_walk", "wait_light"]
    lights_to_use, lamp_dict = load_lamp_conf('test_conf.txt')

    if "red" in lights_to_use:
        red_cycle = lamp_dict['red']
        red_thread = threading.Thread(target=red_light, args=("on",5,))#, daemon=True)
        red_thread.start()
    if "amber" in lights_to_use:
        amber_cycle = lamp_dict['amber']
        amber_thread = threading.Thread(target=amber_light, args=("on",2,))#, daemon=True)
        amber_thread.start()
    if "green" in lights_to_use:
        green_cycle = lamp_dict['green']
        green_thread = threading.Thread(target=green_light, args=(green_cycle[g_cycle][0],green_cycle[g_cycle][1]))
        green_thread.start()
    if "walk_light" in lights_to_use:
        walk_cycle = lamp_dict['walk']
        walk_thread = threading.Thread(target=walk_light, args=(walk_cycle[g_cycle][0],walk_cycle[g_cycle][1]))
        walk_thread.start()
    if "dont_walk" in lights_to_use:
        dontwalk_thread = threading.Thread(target=dontwalk_light, args=(dontwalk_cycle[dw_cycle][0],dontwalk_cycle[dw_cycle][1]))
        dontwalk_thread.start()
    if "wait_light" in lights_to_use:
        wait_thread = threading.Thread(target=wait_light, args=(wait_cycle[wt_cycle][0],wait_cycle[wt_cycle][1]))
        wait_thread.start()
    # Start the loop
    while True:
        # Red Thread
        if "red" in lights_to_use:
            if not red_thread.is_alive():
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
        # walk thread
        if "walk_light" in lights_to_use:
            if not walk_thread.is_alive():
                w_cycle = w_cycle + 1
                if w_cycle > len(walk_cycle)-1:
                    w_cycle = 0
                walk_thread = threading.Thread(target=walk_light, args=(walk_cycle[w_cycle][0],walk_cycle[w_cycle][1]))
                walk_thread.start()
        # dontwalk thread
        if "dont_walk" in lights_to_use:
            if not dontwalk_thread.is_alive():
                dw_cycle = dw_cycle + 1
                if dw_cycle > len(dontwalk_cycle)-1:
                    dw_cycle = 0
                dontwalk_thread = threading.Thread(target=dontwalk_light, args=(dontwalk_cycle[dw_cycle][0],dontwalk_cycle[dw_cycle][1]))
                dontwalk_thread.start()
        # wait thread
        if "wait_light" in lights_to_use:
            if not wait_thread.is_alive():
                wt_cycle = wt_cycle + 1
                if wt_cycle > len(wait_cycle)-1:
                    wt_cycle = 0
                wait_thread = threading.Thread(target=wait_light, args=(wait_cycle[wt_cycle][0],wait_cycle[wt_cycle][1]))
                wait_thread.start()
