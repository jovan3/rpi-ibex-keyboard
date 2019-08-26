# Keyboard configuration
## How the keyboard works

The integrated keyboard on the rpi-ibex board does not use a keyboard controller that's supported by the Linux kernel. Instead, it uses an Atmega328PB microcontroller, which acts as a keyboard controller. The microcontroller passes keyboard events to the Raspberry Pi using I2C. Whenever a button is pressed on the keyboard, an interrupt signal is sent on a GPIO pin. A program running on Raspbian handles that interrupt and reads from the I2C slave device (the keyboard). The keyboard will send info about the event - which button was pressed or released. The program will generate a uinput keyboard event accordingly.

## Loding the uinput Linux module

Add ```uinput`` in a newline to the ```/etc/modules``` file.

## Systemd service

Create a file with path ```/lib/systemd/system/rpi-ibex-keyboard.service``` and with the following content:

```
[Unit]
Description=rpi-ibex keyboard uinput bridge
DefaultDependencies=no
Before=local-fs-pre.target
Wants=local-fs-pre.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/pi/rpi-ibex/gpio.py
RemainAfterExit=yes

[Install]
WantedBy=sysinit.target
```

Run ```sudo systemctl enable rpi-ibex-keyboard.service``` to enable the service when booting.