# tinypixel

Host neopixel control


## Install service
```shell
# enable i2c, rpi setup
echo i2c-dev | sudo tee -a /etc/modules
# uncomment (or add) following lines in /boot/config.txt
# dtparam=i2c_arm=on
# dtparam=i2s=on 

sudo apt update
sudo apt install -y git python3-dev python3-virtualenv libi2c-dev python3-smbus
pip install --upgrade pip

reboot


cd <klipper-env>
./bin/pip install smbus2

cd <moonraker-env>
./bin/pip install smbus2

cd ~
git clone https://github.com/vertexbz/tinypixel.git

# Klipper
cd ~/tinypixel
ln -s ./extension/tinypixel <klipper repo>/klippy/extras/
ln -s ./extension/dummypixel.py <klipper repo>/klippy/extras/

# Klipper
cd ~/tinypixel
ln -s ./extension/tinypixel <moonraker repo>/moonraker/components/

# CLI
cd ~/tinypixel
virtualenv -p python3 ~/tinypixel-env
~/tinypixel-env/bin/pip install -r ./requirements.txt
cp ./tp-cli ~/tinypixel-env/bin/
sudo ln -s ~/tinypixel-env/bin/tp-cli /usr/local/bin/tp-cli
```

## Extension

### Set up as moonraker extension

#### Configuration

```
[tinypixel lights]
bus: 1
# retries: 5
channel: 0
chain_count: 50
color_order: GRB
```

#### Usage

#### Install klipper dummypixel extension
```
[dummypixel lights]
chain_count: 50
```

##### Usage
```
SET_LED LED="lights" RED=1 GREEN=0 BLUE=0.0314 INDEX=9 TRANSMIT=1
```

### Set up as Klipper extension

#### Installation
```
[tinypixel lights]
bus: 1
# retries: 5
channel: 0
chain_count: 50
color_order: GRB
```

#### Usage
```
SET_LED LED="lights" RED=1 GREEN=0 BLUE=0.0314 INDEX=9 TRANSMIT=1
```