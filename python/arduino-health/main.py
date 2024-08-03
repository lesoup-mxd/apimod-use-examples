"""
    This script fetches the health level from a local server and sends it to an Arduino over serial, using a single byte with no line ending.
    The health level is expected to be a float in the range 0 to 20, which is then mapped to a byte in the range 0 to 255.

    The arduino itself should be listening for up to 3 characters that represent the health level in decimal format, followed by a newline character.
"""

import requests
import serial
import time

def write_ser(x, ser):
    ser.write(bytes(x, 'utf-8'))  # Send data to Arduino
    time.sleep(0.05)  # Short delay to allow Arduino to process
    return None

def get_health_level():
    url = "http://localhost:8080/hello"
    response = requests.get(url)
    if response.status_code == 200: #"OK"
        data = response.json()
        health_level = data.get("health") #Health key
        if health_level is not None:
            # Directly use the health level as it's within 0-20 (Should be a float in the json response)
            print(f"Health level: {health_level}")
            return float(health_level)
    else:
        print(f"Failed to fetch health level, status code: {response.status_code}")
        return None

if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        while True: #Main loop
            health_level = get_health_level()
            if health_level is not None:
                write_ser(
                    str(
                        int(health_level * 12.75)),
                    ser=ser)  # Map health level to 0-255 and send to Arduino
            time.sleep(1)  # Delay
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()
