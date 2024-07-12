"""***************************************************************************
*                                                                            *
*                      UAXSAT IV Project - 2024                              *
*                  Developed by Javier Bolaños Llano                         *
*                 https://github.com/javierbolanosllano                      *
*                                                                            *
***************************************************************************"""

# icm20948module.py
import time
import board
import adafruit_icm20x

# Función para inicializar el sensor ICM
def initialize_sensor():
    i2c = board.I2C()  # Utiliza board.SCL y board.SDA por defecto
    icm = adafruit_icm20x.ICM20948(i2c)
    return icm

# Función para obtener datos de aceleración
def read_acceleration(icm):
    return icm.acceleration

# Función para obtener datos de giroscopio
def read_gyro(icm):
    return icm.gyro

# Función para obtener datos del magnetómetro
def read_magnetic(icm):
    return icm.magnetic

def read_sensor_data(icm):
    try:
        acceleration, gyro, magnetic = read_acceleration(icm), read_gyro(icm), read_magnetic(icm)
        return {"acceleration": acceleration, "gyro": gyro, "magnetic": magnetic}
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None
    
# Función principal para ejecución continua
def main():
    icm = initialize_icm_sensor()
    while True:
        sensor_data = read_sensor_data(icm)
        if sensor_data:
            print(f"Acceleration: {sensor_data['acceleration']}, Gyro: {sensor_data['gyro']}, Magnetic: {sensor_data['magnetic']}")
        else:
            print("Error initializing the sensor")
        time.sleep(1)

# Ejecutar el sensor si se ejecuta como script principal
if __name__ == "__main__":
    main()

