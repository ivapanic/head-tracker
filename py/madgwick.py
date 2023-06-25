from ctypes import *

class quaternion(Structure):
    _fields_ = [
        ("q1", c_float),
        ("q2", c_float),
        ("q3", c_float),
        ("q4", c_float)
    ]

class madgwick:
    def __init__(self):
        self.mad_lib = cdll.LoadLibrary("./madgwick.dll")

        self.mad_lib.begin.argtypes = [c_float]
        self.mad_lib.begin.restype = None
        
        self.mad_lib.update.argtypes = [c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float, c_float]
        self.mad_lib.update.restype = None

        self.mad_lib.updateIMU.argtypes = [c_float, c_float, c_float, c_float, c_float, c_float]
        self.mad_lib.updateIMU.restype = None

        self.mad_lib.getRoll.argtypes, self.mad_lib.getPitch.argtypes, self.mad_lib.getYaw.argtypes = [], [], []
        self.mad_lib.getRoll.restype, self.mad_lib.getPitch.restype, self.mad_lib.getYaw.restype = c_float, c_float, c_float


    def filter (self, acc : list, gyro : list, mag : list) -> None:
        self.mad_lib.begin(10)
        if len(mag) != 0:
            self.ahrs_filter(acc, gyro, mag)
        else:
            self.imu_filter(acc, gyro)

    def ahrs_filter(self, acc : list, gyro : list, mag : list) -> None:
        self.mad_lib.update(gyro[0], gyro[1], gyro[2], acc[0], acc[1], acc[2], mag[0], mag[1], mag[2])

    def imu_filter(self, acc : list, gyro : list) -> None:
        self.mad_lib.updateIMU(gyro[0], gyro[1], gyro[2], acc[0], acc[1], acc[2])
    
    def euler_angles(self) -> list:
        return [self.mad_lib.getRoll(), self.mad_lib.getPitch(), self.mad_lib.getYaw()]
    