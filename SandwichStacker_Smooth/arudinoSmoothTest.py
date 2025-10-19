import serial
import time
serial1 = serial.Serial('/dev/ttyUSB0', 9600)

def reset():
    serial1.write(b'base,90\n')
    time.sleep(5)
    serial1.write(b'elbow,90\n')
    time.sleep(5)
    serial1.write(b'shoulder,140\n')
    time.sleep(5)
    serial1.write(b'wrist,100\n')
    time.sleep(5)
    serial1.write(b'hand,180\n')
    print('reset done')

def pickup():
    print("pickup done")
    
    
serial1.write(b'base,0\n')
time.sleep(5)
serial1.write(b'elbow,30\n')
time.sleep(5)
serial1.write(b'shoulder,100\n')
time.sleep(5)
serial1.write(b'wrist,0\n')
time.sleep(5)
serial1.write(b'hand,180\n')
print('done')

time.sleep(3)
reset()
time.sleep(3)
pickup()

    
