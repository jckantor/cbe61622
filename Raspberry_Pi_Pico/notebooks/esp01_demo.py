from machine import Pin
from esp8266 import ESP8266
import time
import sys

esp01 = ESP8266(txPin=16, rxPin=17)