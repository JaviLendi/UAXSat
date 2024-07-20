"""* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
*                                                                            *
*                    Developed by Javier Lendínez                            *
*                    https://github.com/javilendi                            *
*                                                                            *
*                      UAXSAT IV Project - 2024                              *
*                   https://github.com/UAXSat/UAXSat                         *
*                                                                            *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"""


import serial
from serial.tools import list_ports
from ublox_gps import UbloxGps
import time
import sys

class GPSHandler:
    def __init__(self, baudrate, timeout, description=None, hwid=None):
        self.baudrate = baudrate
        self.timeout = timeout
        self.description = description
        self.hwid = hwid
        self.port = self.find_gps_port(description, hwid)
        self.gps, self.serial_port = self.initialize_gps()

    def find_gps_port(self, description, hwid):
        ports = list_ports.comports()
        for port in ports:
            if description and description in port.description:
                return port.device
            if hwid and hwid in port.hwid:
                return port.device
        return None

    def initialize_gps(self):
        if not self.port:
            return None, None
        try:
            serial_port = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
            gps = UbloxGps(serial_port)
            return gps, serial_port
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return None, None

    def GPSprogram(self):
        if self.gps is None or self.serial_port is None:
            print("GPS initialization failed.")
            return

        try:
            while True:
                data = {
                    'Latitude': None,
                    'Longitude': None,
                    'Altitude': None,
                    'Heading of Motion': None,
                    'Roll': None,
                    'Pitch': None,
                    'Heading': None,
                    'NMEA Sentence': None,
                }
                try:
                    geo = self.gps.geo_coords()
                    veh = self.gps.veh_attitude()
                    stream_nmea = self.gps.stream_nmea()
                    hp_geo = self.gps.hp_geo_coords()

                    if geo is not None:
                        data['Latitude'] = geo.lat
                        data['Longitude'] = geo.lon
                        data['Altitude'] = geo.height/1000
                        data['Heading of Motion'] = geo.headMot
                        #print(data['Latitude'], data['Longitude'], data['Altitude'], data['Heading of Motion'])
                    else:
                        print("No GPS geo fix acquired.")

                    if veh is not None:
                        data['Roll'] = veh.roll
                        data['Pitch'] = veh.pitch
                        data['Heading'] = veh.heading
                        #print(data['Roll'], data['Pitch'], data['Heading'])
                    else:
                        print("No vehicle attitude acquired.")

                    if stream_nmea is not None:
                        data['NMEA Sentence'] = stream_nmea
                        #print(data['NMEA Sentence'])
                    else:
                        print("No NMEA sentence acquired.")

                    if hp_geo is not None:
                        data['Latitude'] = hp_geo.latHp
                        data['Longitude'] = hp_geo.lonHp
                        data['Altitude'] = hp_geo.heightHp/1000
                        #print(data['Latitude'], data['Longitude'], data['Altitude'])
                    else:
                        print("No high precision geo fix acquired.")
                    
                    return data
                    
                except (ValueError, IOError) as err:
                    print(f"GPS error: {err}")
                    return None
        
        except KeyboardInterrupt:
            self.serial_port.close()
            print("GPS stopped.")

if __name__ == '__main__':
    gps_handler = GPSHandler(baudrate=38400, timeout=1, description=None, hwid="1546:01A9")
    try:
        while True:
            gps_handler.GPSprogram()
            time.sleep(1)  # Add a small delay to prevent CPU overuse
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    
