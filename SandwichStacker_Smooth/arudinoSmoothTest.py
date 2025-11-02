import serial
import time
serial1 = serial.Serial('/dev/ttyUSB0', 9600)

def reset():
    serial1.write(b'base,90\n')
    time.sleep(0.5)
    serial1.write(b'shoulder,140\n')
    time.sleep(0.5)
    serial1.write(b'elbow,90\n')
    time.sleep(0.5)
    serial1.write(b'wrist,100\n')
    time.sleep(0.5)
    serial1.write(b'hand,180\n')
    print('reset done')

def pickup():
    reset()
    print("Picking up")
    #rotate elbow so arm pointing up
    serial1.write(b'elbow,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,160\n')
    time.sleep(1)
    #open hand
    serial1.write(b'hand,00\n')
    time.sleep(1)
    #rotate wrist
    serial1.write(b'wrist,30\n')
    time.sleep(1)
    #shoulder + elbow reach down
    serial1.write(b'elbow,40\n')
    time.sleep(1)
    serial1.write(b'shoulder,80\n')
    time.sleep(1)
    #close hand
    serial1.write(b'hand,180\n')
    time.sleep(1)
    #shoulder/elbow lift up
    serial1.write(b'shoulder,140\n')
    time.sleep(1)
    serial1.write(b'elbow,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,75\n')
    time.sleep(1)
    #reach back down
    serial1.write(b'elbow,50\n')
    time.sleep(1)
    serial1.write(b'shoulder,110\n')
    time.sleep(1)
    #open hand
    serial1.write(b'hand,0\n')
    time.sleep(1)
    print("Pickup complete")
    time.sleep(5)
    #reset
    reset()
    
def pushaway():
    reset()
    print("Pushing Away")
    #rotate elbow so arm pointing up
    serial1.write(b'elbow,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,180\n')
    time.sleep(1)
    #shoulder + elbow reach down
    serial1.write(b'elbow,40\n')
    time.sleep(1)
    serial1.write(b'shoulder,80\n')
    time.sleep(1)
    #rotate wrist
    serial1.write(b'wrist,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,75\n')
    time.sleep(1)
    print("Pushaway complete")
    time.sleep(5)
    #reset
    reset()

    
pushaway()
    
#pickup()