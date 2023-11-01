# tinypixel

Host neopixel control


## Install service
```shell
sudo apt update
sudo apt install -y git python3-dev python3-virtualenv libi2c-dev python3-smbus
pip install --upgrade pip

# enable i2c, rpi setup
echo i2c-dev | sudo tee -a /etc/modules
# uncomment (or add) following lines in /boot/config.txt
# dtparam=i2c_arm=on
# dtparam=i2s=on 

cd ~
git clone <REPO>

virtualenv -p python3 ~/tinypixel-env
~/tinypixel-env/bin/pip install -r ~/tinypixel/requirements.txt


reboot
```

## Extension

### Install as moonraker extension

#### Installation

```
[tinypixel lights]
socket: /tmp/tinypixel
channel: 0
```

#### Usage

#### Install klipper dummypixel extension
```
[dummypixel lights]
socket: /tmp/tinypixel
channel: 0
```
or
```
[dummypixel lights]
chain_count: 50
```

### Klipper extension

#### Installation
```
[tinypixel lights]
socket: /tmp/tinypixel
channel: 0
```

#### Usage
