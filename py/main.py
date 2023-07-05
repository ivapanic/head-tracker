import argparse

from madgwick import madgwick
from parsers import parse_imu_data
from ble_central import ble_central
from osc_client import osc_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Head tracking bridge', 
                                     description='This program receives IMU data via BLE connection, parses it,\
                                     calculates head orientation and sends information to the wanted plugin (IEM Suite, Sparta).')
    parser.add_argument('-pin', '--plugin', type=str, default='sparta', help="Name of the plugin you want to send data to.\
                        If it's an IEM Suite plugin, write the name of the plugin. Eg. 'SceneRotator'.")
    parser.add_argument('-ip', '--ip_address', type=str, default='127.0.0.1', help="IP address of the server.")
    parser.add_argument('-p', '--port', type=int, required=True, help="UDP port to send OSC data to, user-defined in the plugin.")
    parser.add_argument('-d', '--dof', type=int, required=False, default=9, choices=[6, 9], help="Number of sensor's degrees of freedom. \
                      6DOF: 3-axis accelerometer and gyroscope.\n9DOF: 3-axis accelerometer, gyroscope and magnetometer.")

    args = parser.parse_args()
    dof = args.dof

    ble_central = ble_central()
    osc_client = osc_client(args.ip_address, args.port, args.plugin)

    ble_central.scan_peripherals()
    connected = ble_central.connect_to_peripheral()
	
    if connected:
        filter = madgwick()
        while True:
            raw_data = parse_imu_data(ble_central.read(), dof)
            filter.filter(raw_data[0], raw_data[1], raw_data[2])
            osc_client.send(filter.euler_angles())
            
