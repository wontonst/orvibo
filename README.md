# orvibo
Module to manipulate Orvibo devices, such as [s20 wifi sockets](http://www.aliexpress.com/item/Orvibo-S20-Wifi-Cell-Phone-Power-Socket-Wireless-Timer-Switch-Wall-Plug-Phone-Wireless-Remote-Control/32357053063.html) and [AllOne IR blasters](http://www.aliexpress.com/item/Orvibo-Allone-Wiwo-R1-Intelligent-house-Control-Center-Smart-Home-WIFI-IR-RF-Wireless-Remote-Switch/32247638788.html) to control whatever devices via emiting IR signal (TVs, AV receivers, air conditioners, etc)


## References
* Lots of info was found in [ninja-allone](https://github.com/Grayda/ninja-allone/blob/master/lib/allone.js) library
* S20 data analysis by anonymous is [here](http://pastebin.com/0w8N7AJD)
* [python-orvibo](https://github.com/happyleavesaoc/python-orvibo) similar module, but currently supports Orvibo S20 sockets only.

## TODO
- [x] Get rid of keeping connection to the Orvibo device, which breaks further discover
- [x] Test under linux platform
- [x] Consider python 2.7 support
- [x] Add mac and type cmd line arguments in order decrease execution latency (ver 1.1)
- [ ] API for adding new Orvibo device to the network
- [ ] Python setup script
- [ ] Orvibo s20 event handler
- [ ] ~~Learning and emiting RF 433MHz signal~~ [Issue#7](https://github.com/cherezov/orvibo/issues/7)

## Requires
* Python (tested on Win7 with python 2.7 and python 3.4 and Ubuntu with python 3.2)
 
## Installation

This package is not on PyPI but you can clone or download this package and run `pip install /path/to/orvibo`

## Known applications
*please let me know about apps not listed here :octocat:*
* [OpenHAB](https://community.openhab.org/t/orvibo-allone-ir-blaster-guide/9111) guide by community user [@robinson](https://community.openhab.org/users/robinson)
* [Samsung Artic](https://www.artik.io/works-with-cloud/orbivo-wiwo/) guide cloud setup
* [Domoticz](http://easydomoticz.com/forum/viewtopic.php?t=2406) community guide

## Usage
### As console app
#### Overview
```shell
orvibo.py [-i <ip>] | [-m <mac> -x <socket/irda>] [-s on|off] | [-t <file_to_save_signal>] | [-e <file_with_signal_to_emit>]]
```
#### Discover all Orvibo devices in the network
```shell
> python orvibo.py
Orvibo[type=socket, ip=192.168.1.45, mac='acdf238d1d2e']
Orvibo[type=irda, ip=192.168.1.37, mac='accf4378efdc']
```
#### Discover device by ip
```shell
> python orvibo.py -i 192.168.1.45
Orvibo[type=socket, ip=192.168.1.45, mac='acdf238d1d2e']
Is enabled: True
```
#### State of known device [draft]
Faster than just discovering by ip, since discovering step is skipped here.
*Note*: There is no any mac/type validation!
```shell
> python orvibo.py -m acdf238d1d2e -x socket
Orvibo[type=socket, ip=unknown, mac='acdf238d1d2e']
Is enabled: True
```
Same arguments can be used for all examples below.
#### Switch s20 wifi socket
```shell
> python orvibo.py -i 192.168.1.45 -s on
Orvibo[type=socket, ip=192.168.1.45, mac='acdf238d1d2e']
Already enabled.
```
#### Grab IR code to file
```shell
> python orvibo.py -i 192.168.1.37 -t test.ir
Orvibo[type=irda, ip=192.168.1.37, mac='accf5378dfdc']
Done
```
#### Emit already grabed IR code
```shell
> python orvibo.py -i 192.168.1.37 -e test.ir
Orvibo[type=irda, ip=192.168.1.37, mac='accf5378dfdc']
Done
```
### As python module
#### Discover all devices in the network
```python
from orvibo import Orvibo

for ip in Orvibo.discover():
    print('IP =', ip)

for args in Orvibo.discover().values():
    device = Orvibo(*args)
    print(device)
```
Result
```
IP = 192.168.1.45
IP = 192.168.1.37
Orvibo[type=socket, ip=192.168.1.45, mac='acdf238d1d2e']
Orvibo[type=irda, ip=192.168.1.37, mac='accf4378efdc']
```

#### Getting exact device by IP
```python
device = Orvibo.discover('192.168.1.45')
print(device)
```
Result:
```
Orvibo[type=socket, ip=192.168.1.45, mac='acdf238d1d2e']
```

#### Control S20 wifi socket
**only for devices with type 'socket'**
```python
device = Orvibo('192.168.1.45')
print('Is socket enabled: {}'.format(device.on))
device.on = not device.on # Toggle socket
print('Is socket enabled: {}'.format(device.on))
```
Result:
```
Is socket enabled: True
Is socket enabled: False
```

#### Learning AllOne IR blaster
**only for devices with type 'irda'**
```python
device = Orvibo('192.168.1.37')
ir = device.learn('test.ir', timeout=15) # AllOne red light is present,
                                           # waiting for ir signal for 15 seconds and stores it to test.ir file
if ir is not None:
    # Emit IR code from "test.ir"
    device.emit('test.ir')
    # Or with the same result
    # device.emit(ir)
```
#### Keeping connection to Orvibo device

By default module doesn't keep connection to the Orvibo device to allow user not thinking about unplanned disconnections from device by whatever reasons (power outage, wifi router reboot, etc). Such behavior actually leads to valuable delay between sending request and applying command on the Orvibo device. Module allows to keep the connection and decrease the latency via setting keep_connection property to True. In this way closing connection and handling socket errors duties lie on orvibo python library user.

```python
import socket

device = Orvibo('192.168.1.45')
device.keep_connection = True

def blink_socket(device):
    try:
        device.on = not device.on
    except socket.error:
        # Reset connection to device    
        device.keep_connection = True

try:
    # Note: now socket errors are handled by user!

    # Blink the socket ^_^
    for i in range(5):
        blink_socket(device)

    # You also may stop using connection anytime
    # device.keep_connection = False
finally:
    # Connection must be closed explicitly.
    # via
    device.close()
    # or via
    # device.keep_connection = False
```
