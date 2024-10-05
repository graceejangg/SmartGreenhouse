# SmartGreenhouse

## Setup
To run the project setup a raspberrypi with a grovepi.
Connect the follwing sensors as described:
    DHT - Temperature and Humidity Sensor   - D8
    Soil Moisture sensor                    - A0
    Light sensor                            - A1

    LED Blue                                - D4
    LED Red                                 - D3
    Relay                                   - D2

    LCD Display                             - I2C-1

- Configure the IP address of the PC in the ```mainPi.py``` file. The variable mqtt_hostname must be the IP address of the PC.

## Execution
- Copy the garden directory to the raspberrypi
- Start the containers on the PC with ```docker compose up --build```
- Start the ```mainPi.py``` script on the pi.


On the PC you can open the influxdb in the browser under ```localhost:8086```

Username is ```admin```
Password is ```administrator```

Under dashboard open the ```garden``` dashboard to see the sensor values.
