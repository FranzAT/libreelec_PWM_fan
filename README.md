<br/>
<p align="center">
  <h1 align="center">LibreELEC PWM Fan</h1>
</p>

![Downloads](https://img.shields.io/github/downloads/FranzAT/libreelec_PWM_fan/total) ![Contributors](https://img.shields.io/github/contributors/FranzAT/libreelec_PWM_fan?color=dark-green) ![Issues](https://img.shields.io/github/issues/FranzAT/libreelec_PWM_fan) ![License](https://img.shields.io/github/license/FranzAT/libreelec_PWM_fan)

## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
    - [Hardware Setup](#hardware-setup)
    - [Software Setup](#software-setup)
    - [Test](#test)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
  - [Creating A Pull Request](#creating-a-pull-request)
- [License](#license)
- [Authors](#authors)
- [Acknowledgements](#acknowledgements)

## About The Project

I was looking to cool my Raspberry Pi which was running LibreELEC.
The Raspberry Pi case was equipped with a 5V fan. 
It was running all the time on full speed when mounted to the 5V pin. It was too loud.

With this open-source project I wanted to:

* Cool the Raspberry Pi only if it is running warm.
* Adapt the fan speed, so that the noise is reduced.
* Play around with transistors.
* Enable program running on LibreELEC.

## Built With

* [Python](https://www.python.org/)

## Getting Started

The available 5V fan has active power of up to 1W. However, the GPIO pins can only deliver 3.3V with a maximum of 1mA each. 
With a NPN transistor it is possible to control the 5V circuit with a low current from a GPIO pin providing voltage of 3.3V.
To control the fan speed, Pulse-width modultion (PWM) is used (available on GPIO 12), with which the average power delivered to the 3.3V circuit can be controlled.

### Prerequisites

#### Hardware Setup
NPN-Transistor: 2N3904
1. Emitter connected to GND.
2. Base connected to GPIO 12 (PWM0) with a 1kOhm resistor in between.
3. Collector connected to fan and fan connected to 5V.
4. Pull-Down 10kOhm resistor between GND and GPIO 12
5. Diode between Collector and 5V (optional to protect transistor from fan)

#### Software Setup
Install on LibreELEC the 'Raspberry Pi Tools' addon </br>
`Addons --> install from repository --> LibreELEC Add-ons --> Program Addons --> Raspberry PiTools`

#### Test
Run python program 'calibrate.py' to change speed via SSH for testing before setting lowest speed in the script.


### Installation

1. save the file 'PWM_fan.py' on your RaspberryPi to
```
/storage/.kodi/userdata/PWM_fan/PWM_fan.py
```
2. and change permission of the PWM_fan.py file with `chmod 777`
3. save the file 'PWM_fan.service' on your RaspberryPi to
```
/storage/.config/system.d/PWM_fan.service
```
4. enable the service with
```
systemctl enable PWM_fan
```
5. start the service with
```
systemctl start PWM_fan
```
6. check if the service is working with
```
systemctl status PWM_fan.service
```

## Usage

1. Start the program as service after each start.
2. The CPU temperature is read.
3. Calculate desired fan speed.
4. Update new fan speed with desired speed.

## Roadmap

See the [open issues](https://github.com/FranzAT/libreelec_PWM_fan/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/FranzAT/libreelec_PWM_fan/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/FranzAT/libreelec_PWM_fan/blob/main/LICENSE) for more information.

## Authors

* **Franz Heinzl** - [https://github.com/FranzAT](https://github.com/FranzAT)

## Acknowledgements

* [LibreELEC Forum: Cooling Fan Control Raspberry Pi Libreelec.](https://forum.libreelec.tv/thread/9472-cooling-fan-control-raspberry-pi-libreelec/)
* [Hackernoon: How to control a fan to cool the CPU of your RaspBerryPi](https://hackernoon.com/how-to-control-a-fan-to-cool-the-cpu-of-your-raspberrypi-3313b6e7f92c)
