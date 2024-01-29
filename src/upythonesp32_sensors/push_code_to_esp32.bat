esptool --chip esp32 --port COM7 erase_flash
esptool --chip esp32 --port COM7 --baud 460800 write_flash -z 0x1000 C:\upython\ESP32_GENERIC-20240105-v1.22.1.bin
ampy --port COM7 put boot.py
ampy --port COM7 put main.py
ampy --port COM7 put hcsr04.py
ampy --port COM7 put umqttsimple.py