# 2.8 ILI9341 TFT SPI display

## Wiring

|Module|Raspberry Pi Zero W|
|---|---|
|SDO/MISO|MISO|
|LED (56Ohm)|GPIO18|
|SCK|SCLK|
|SDI/MOSI|MOSI|
|DC/RS|GPIO24|
|RESET|GPIO25|
|CS|SPI-EN0|
|GND|GND|
|Vcc|3.3V|


## Kernel module

The fbtft_device kernel module can be used with this display. To load the driver with modprobe:

```
modprobe fbtft_device name=fb_ili9341 gpios=reset:25,dc:24,led:18 custom speed=16000000 bgr=1 rotate=90
```

The following will appear in dmesg:

```
[    8.325004] fbtft_device: GPIOS used by 'fb_ili9341':
[    8.334749] fbtft_device: 'reset' = GPIO25
[    8.343213] fbtft_device: 'dc' = GPIO24
[    8.351292] fbtft_device: 'led' = GPIO18
[    8.359376] spi spi0.1: spidev spi0.1 125000kHz 8 bits mode=0x00
[    8.369569] spi spi0.0: fb_ili9341 spi0.0 16000kHz 8 bits mode=0x00
```

Change the `gpios` values of the option if you want to change any of the reset, dc or led pins. To load the module on startup create a /etc/modules-load.d/fbtft.conf file with the following content:

```
spi-bcm2835
fbtft_device
```

To pass all the required parameters to the fbtft_device module create a file /etc/modprobe.d/fbtft.conf with the following content:

```
options fbtft_device name=fb_ili9341  gpios=reset:25,dc:24,led:18 custom speed=16000000 rotate=90 bgr=1
```
After loading the fbtft_device module a framebuffer device will be created (/dev/fb1).

## Framebuffer stuff

To create a mapping between a tty console and a framebuffer device use con2fbmap:

```
Usage: con2fbmap console [framebuffer]
Example: con2fbmap 1 1
```