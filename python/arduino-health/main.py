"""
    This script fetches the health level from a local server and sends it to an Arduino over serial, using a single byte with no line ending.
    The health level is expected to be a float in the range 0 to 20, which is then mapped to a byte in the range 0 to 255.

    The arduino itself should be listening for up to 3 characters that represent the health level in decimal format, followed by a newline character.

    !!IMPORTANT!!:
     Make sure that the serial port is correct and accessible, on UNIX systems it's usually /dev/ttyUSB<port> or /dev/ttyACM<port>, on Windows it's usually COM<port>
     I had to allow access to the serial port on my system by running the following command after connecting the Arduino:
     sudo chmod a+rw /dev/ttyUSB0
        Replace /dev/ttyUSB0 with the actual serial port if necessary.
        Might work differently for you, so make sure to check the serial port permissions on your system. And read the documentation for the pyserial library / your system's serial port configuration.
"""

import requests
import serial
import time

def write_ser(x, ser):
    ser.write(bytes(x, 'utf-8'))  # Send data to Arduino
    time.sleep(0.05)  # Short delay to allow Arduino to process

def get_health_level():
    url = "http://localhost:8080/hello" #Disclaimer: the endpoint may change as the project evolves
    response = requests.get(url)
    if response.status_code == 200: #"OK"
        data = response.json()
        health_level = data.get("health") #Health key
        #For debugging purposes
        #health_level = 20 #Debug !
        if health_level is not None:
            # Directly use the health level as it's within 0-20 (Should be a float in the json response)
                print(f"Health level: {health_level}") #Debug
                return float(health_level)
    else:
        print(f"Failed to fetch health level, status code: {response.status_code}")
        return None

if __name__ == "__main__":
    try:
        health_level = 5
        new_health_level = 0
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        time.sleep(1.5)  # Wait for Arduino to reset
        write_ser('0\n', ser)  # Send 0 to Arduino to reset the health level
        while True: #Main loop
              # Delay
            new_health_level = get_health_level()
            if health_level == new_health_level:
                time.sleep(.3)
                continue
            time.sleep(.5)
            health_level = new_health_level


            if health_level is not None:
                write_ser(
                    (str(int(health_level * 12.75))+'\n'),
                    ser=ser)  # Map health level to 0-255 and send to Arduino
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()
