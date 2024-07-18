import serial
from serial.tools import list_ports
from ublox_gps import UbloxGps

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

    def run(self):
        if self.gps is None or self.serial_port is None:
            print("GPS initialization failed.")
            return

        try:
            print("Listening for UBX Messages")
            while True:
                try:
                    geo = self.gps.geo_coords()
                    veh = self.gps.veh_attitude()
                    stream_nmea = self.gps.gps.stream_nmea()

                    if geo is not None:
                        print("Longitude: ", geo.lon)
                        print("Latitude: ", geo.lat)
                        print("Heading of Motion: ", geo.headMot)

                    if veh is not None:
                        print("Roll: ", veh.roll)
                        print("Pitch: ", veh.pitch)
                        print("Heading: ", veh.heading)

                    if stream_nmea is not None:
                        print(stream_nmea)

                    else:
                        print("No GPS fix acquired.")
                    
                except (ValueError, IOError) as err:
                    print(f"GPS error: {err}")
        
        finally:
            self.serial_port.close()

if __name__ == '__main__':
    gps_handler = GPSHandler(baudrate=38400, timeout=1, description=None, hwid="1546:01A9")
    gps_handler.run()
