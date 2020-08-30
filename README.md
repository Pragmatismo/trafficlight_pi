# trafficlight_pi

Simple control for relay controlled traffic lights, and glitched traffic lights.


# GPIO Numbers 

Can control relays, motors, LEDs, or anything that uses a digital on-off signal from the GPIO

Green = 7
Amber = 8
Red   = 25
Walk  = 24
dontwalk = 23
wait = 18

# Start-up

To start on boot add this line to cron

@reboot /home/pi/trafficlight_pi/traffic_loop.py

or

@reboot /home/pi/trafficlight_pi/traffic_glitch.py

