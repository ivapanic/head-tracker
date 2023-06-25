#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

// ------------------------------------------ BLE UUIDs ------------------------------------------
#define BLE_UUID_PERIPHERAL "19B10000-E8F2-537E-4F6C-D104768A1214"
#define BLE_UUID_CHARACT_LED "19B10001-E8F2-537E-4F6C-E104768A1214"
#define BLE_UUID_CHARACT_IMU "29B10001-E8F2-537E-4F6C-a204768A1215"


BLEService IMU_Service(BLE_UUID_PERIPHERAL);

BLEByteCharacteristic  switch_characteristic(BLE_UUID_CHARACT_LED, BLERead | BLEWrite);
BLEStringCharacteristic imu_characteristic(BLE_UUID_CHARACT_IMU, BLERead | BLENotify | BLEWrite, 64);

const int led_pin = LED_BUILTIN;

float acc[3];
float gyro[3];
float mag[3];

float acc_start[3];
float gyro_start[3];
float mag_start[3];

float acc_off[] = { 0.0, 0.0, 0.0 };
float gyro_off[] = { 0.0, 0.0, 0.0 };
float mag_off[] = { 0.0, 0.0, 0.0 };

bool is_calibrated = false;
int num_calibration_samples = 500;

// ------------------------------------------ VOID SETUP ------------------------------------------
void setup() 
{
  Serial.begin(115200);

  innit_mate();

  setup_BLE();
  BLE.advertise();

  Serial.println("BLE Peripheral");
}

// ------------------------------------------ VOID LOOP ------------------------------------------
void loop() 
{
  BLEDevice central = BLE.central();

  if (central) 
  {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) 
    {
      if (!is_calibrated)
        calibrate();
      else 
      {
        IMU.readAcceleration(acc[0], acc[1], acc[2]);
        IMU.readGyroscope(gyro[0], gyro[1], gyro[2]);
        IMU.readMagneticField(mag[0], mag[1], mag[2]);
      
        String imu_data = String(acc[0] + acc_off[0], 2) + "," + String(acc[1] + acc_off[1], 2) + "," + String(acc[2] + acc_off[2], 2) + "," 
                        + String(gyro[0] + gyro_off[0], 2) + "," + String(gyro[1] + gyro_off[1], 2) + "," + String(gyro[2] + gyro_off[2], 2) + ","
                        + String(mag[0] + mag_off[0], 2) + "," + String(mag[1] + mag_off[1], 2) + "," + String(mag[2] + mag_off[2], 2);

        add_padding(imu_data);

        imu_characteristic.writeValue(imu_data);
        Serial.println(imu_data)
    }
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}

// --------------------------------------- FUNCTIONS ------------------------------------------
void innit_mate() {
  if (!IMU.begin()) 
  {
    Serial.println("Failed to initialize IMU!");
    while (true);
  }

  // set LED pin to output mode
  pinMode(led_pin, OUTPUT);

  if (!BLE.begin()) 
  {
    Serial.println("starting BLE failed!");
    while (true);
  }
}

void setup_BLE() {
  BLE.setLocalName("BLE_IMU");
  BLE.setAdvertisedService(IMU_Service);

  IMU_Service.addCharacteristic(switch_characteristic);
  IMU_Service.addCharacteristic(imu_characteristic);

  BLE.addService(IMU_Service);

  switch_characteristic.writeValue(0);
}

void add_padding(String& imu_data)
{
    int len = 64 - imu_data.length();

    if (len != 0)
    {
        for (int i = 0; i < len; ++i)
        {
          imu_data += "#";
        }
    }         
}

void calibrate() {
  Serial.println("Calibrating IMU... Please keep the sensor still.");
  float acc_sum[] = { 0.0, 0.0, 0.0 };
  float gyro_sum[] = { 0.0, 0.0, 0.0 };
  float mag_sum[] = { 0.0, 0.0, 0.0 };

  for (int sample = 0; sample < num_calibration_samples; ++sample) {
    IMU.readAcceleration(acc[0], acc[1], acc[2]);
    IMU.readGyroscope(gyro[0], gyro[1], gyro[2]);
    IMU.readMagneticField(mag[0], mag[1], mag[2]);

    for (int i = 0; i < 3; ++i) {
      acc_sum[i] += acc[i];
      gyro_sum[i] += gyro[i];
      mag_sum[i] += mag[i];
    }
  }

  for (int i = 0; i < 3; ++i) {
    acc_off[i] = acc_sum[i] / num_calibration_samples;
    gyro_off[i] = gyro_sum[i] / num_calibration_samples;
    mag_off[i] = mag_sum[i] / num_calibration_samples;

  }

  is_calibrated = true;
  Serial.println("IMU calibration finished.");
}