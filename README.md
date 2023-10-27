# hostpixel

Host neopixel control


## Install service
```shell
sudo apt update
sudo apt install -y git python3-dev python3-virtualenv libi2c-dev python3-smbus
pip install --upgrade pip

cd ~
git clone <REPO>

virtualenv -p python3 ~/hostpixel-env
~/hostpixel-env/bin/pip install -r ~/hostpixel/requirements.txt
sudo cp hostpixel.service /etc/systemd/system/ 
cp hostpixel.conf ~/printer_data/config/
```

## Extension

### Install as moonraker extension

#### Installation

```
[hostpixel lights]
socket: /tmp/hostpixel
channel: 0
```

#### Usage

#### Install klipper dummypixel extension
```
[dummypixel lights]
socket: /tmp/hostpixel
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
[hostpixel lights]
socket: /tmp/hostpixel
channel: 0
```

#### Usage
