import simplepyble

class ble_central:
    def __init__(self):
        self.__select_adapter()
        
    def __select_adapter(self):
        adapters = simplepyble.Adapter.get_adapters()

        if len(adapters) == 0:
            print("No adapters found")

        # Query the user to pick an adapter
        print("Please select an adapter:")
        for i, adapter in enumerate(adapters):
            print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

        choice = int(input("Enter choice: "))
        self.adapter = adapters[choice]

        print(f"Selected adapter: {self.adapter.identifier()} [{self.adapter.address()}]")
    
    def scan_peripherals(self) -> None:
        self.adapter.set_callback_on_scan_start(lambda: print("Scan started."))
        self.adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
        self.adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

        peripherals = []
        while len(peripherals) == 0:
            # Scan for 5 seconds
            print("Scanning for peripherals...")
            self.adapter.scan_for(5000)
            peripherals = self.adapter.scan_get_results()
            
        # Query the user to pick a peripheral
        print("Please select a peripheral:")
        for i, peripheral in enumerate(peripherals):
            print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")
            
        choice = int(input("Enter choice: "))
        self.peripheral = peripherals[choice]

    def connect_to_peripheral(self):
        print(f"Connecting to: {self.peripheral.identifier()} [{self.peripheral.address()}]")
        self.peripheral.connect()

        print("Successfully connected, listing services...")
        services = self.peripheral.services()
        service_characteristic_pair = []

        if len(services) == 0:
            return False
        
        for service in services:
            for characteristic in service.characteristics():
                service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

        # Query the user to pick a service/characteristic pair
        print("Please select a service/characteristic pair:")
        for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
            print(f"{i}: {service_uuid} {characteristic}")

        choice = int(input("Enter choice: "))
        self.service_uuid, self.characteristic_uuid = service_characteristic_pair[choice]

        return True
    
    def read(self) -> bytearray:
        return self.peripheral.read(self.service_uuid, self.characteristic_uuid)
    
    def disconnect(self) -> None:
        self.peripheral.disconnect()
    
