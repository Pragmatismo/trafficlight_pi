# trafficlight_pi

Simple control for relay controlled traffic lights. 

# GPIO Numbers 

Green = 7
Amber = 8
Red   = 25
Walk  = 24
dontwalk = 23
wait = 18

# Start-up

To start on boot add this line to cron

@reboot /home/pi/trafficlight_pi/traffic_loop.py

