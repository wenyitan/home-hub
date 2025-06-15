import adafruit_dht
import board
from gpiozero import RGBLED
from miio import Device, ChuangmiCamera
from miio import AirHumidifierJsqs
from config import get_device_info

class HomeHub:
    def __init__(self):
        self.devices = {
            "dht11": adafruit_dht.DHT11(board.D4),
            # "rgb": RGBLED(red=16, green=20, blue=21, active_high=False, pwm=True),
            "humidifier": AirHumidifierJsqs(ip=get_device_info("humidifier", "ip"), token=get_device_info("humidifier", "token"), timeout=25),
        }

    def get_device(self, label):
        return self.devices[label]