from pythonosc import udp_client

class osc_client:
    def __init__(self, ip_address : str, port : int, software : str):
        self.software = software
        self.client = udp_client.SimpleUDPClient(ip_address, port)
    
    def send(self, data : str) -> None:
        begin_msg = "/ypr"
        if self.software != "sparta":
            begin_msg = f"/{self.software}/ypr"
        
        self.client.send_message(begin_msg, data)
    

    
