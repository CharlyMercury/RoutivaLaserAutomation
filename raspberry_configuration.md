### An option to enable SSH (using terminal commands):

Faster than playing with `raspi-config` is just enabling the service and starting it from the console, so make this quick:

1. Hit `CTRL+ALT+F1` to switch to console (tty1).
2. Enable SSH daemon:

```bash
sudo systemctl enable ssh.service
```

3. Start `sshd` daemon:

```bash
sudo systemctl start ssh.service
```

### Enabling multiples Wifis with static IP:

0. Add 8.8.8.8 to nameserver in /etc/resolv.conf

```bash
sudo nano /etc/resolv.conf
```

```nano
nameserver 8.8.8.8
```


1. Add the following to interfaces

```bash
sudo nano /etc/network/interfaces
```

# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source /etc/network/interfaces.d/*

auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp

iface IZZI-6D04 inet static
address 192.168.0.192
netmask 255.255.255.0
gateway 192.168.0.1

iface CharlyMercury inet static
address 192.168.103.192
netmask 255.255.255.0
gateway 192.168.103.122

iface INFINITUM2A5B_2.4 inet static
address 192.168.1.192
netmask 255.255.255.0
gateway 192.168.1.254

2. Add Wifi's Credentials to wpa_supplicant 

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

and add the following

country=MX
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="IZZI-6D04"
psk="F0AF85386D04"
id_str="IZZI-6D04"
}
network={
ssid="INFINITUM2A5B_2.4"
psk="FMxMFmE237"
id_str="INFINITUM2A5B_2.4"
}
network={
ssid="CharlyMercury"
psk="1234567890"
id_str="CharlyMercury"
}

3. Reboot the Raspberry

```bash
sudo reboot
```

### Configurate Mosquitto Broker

0. Install Mosquitto Broker

```bash
sudo apt update && sudo apt upgrade
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
mosquitto -v
```

1. In Raspberry, For Local mqtt broker I have the following configuration in

    - $ sudo nano /etc/mosquitto/mosquitto.conf

2. Add the following lines to the file

    - allow_anonymous true
    - listener 1883

3. Restart the service

    - $ sudo service mosquitto restart

4. Verify the configuration:

    - $ sudo netstat -tulpn | grep 1883

5. Mqtt client subscriber

    - $ mosquitto_sub -h 192.168.0.192 -p 1883 -t my/topic

6. Mqtt client publisher

    - $ mosquitto_pub -h 192.168.0.192 -p 1883 -t "my/topic" -m "Hello, MQTT!"

