from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=27, trigger=17)

try:
    while True:
        print(f"distance: {sensor.distance * 100:.1f} cm")
        sleep(1)
        
except KeyboardInterrupt:
    print("Stopping...") 