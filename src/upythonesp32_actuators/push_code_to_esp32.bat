esptool --chip esp32 --port COM5 erase_flash
esptool --chip esp32 --port COM5 --baud 460800 write_flash -z 0x1000 C:\upython\ESP32_GENERIC-20240105-v1.22.1.bin
ampy --port COM5 put boot.py
ampy --port COM5 put main.py
ampy --port COM5 put umqttsimple.py