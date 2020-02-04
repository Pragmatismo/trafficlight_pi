# trafficlight_pi

Simple control for relay controlled traffic lights. 

Green = 7
Amber = 8
Red   = 25
Walk  = 24
dontwalk = 28
wait = 26

To start on boot add this line to cron

@reboot /home/pi/trafficlight_pi/traffic_loop.py

