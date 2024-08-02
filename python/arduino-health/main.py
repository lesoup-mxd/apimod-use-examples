import requests
import serial
import time

def get_health_level():
    url = "http://localhost:8080/hello"
    response = requests.get(url)
    if response.status_code == 200: #"OK"
        data = response.json()
        health_level = data.get("healthLevel") #Health key
        if health_level is not None:
            # Directly use the health level as it's within 0-20 (Should be a float in the json response)
            return int(health_level)
    else:
        print(f"Failed to fetch health level, status code: {response.status_code}")
        return None

def send_to_arduino(health_level):
    # Assuming the Arduino is listening on COM3 with b-rate 9600
    ser = serial.Serial('COM3', 9600)
    if ser.isOpen():
        health_bytes = health_level.to_bytes(1, 'big') # Convert 0-20 to a byte
        ser.write(health_bytes)
        ser.close()

if __name__ == "__main__":
    try:
        while True: #Main loop
            health_level = get_health_level()
            if health_level is not None:
                send_to_arduino(health_level)
            time.sleep(1)  # Delay
    except KeyboardInterrupt:
        print("Exiting...")
