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

Add that line to ```/etc/rc.local``` to set fb1 as coonsole framebuffer device.

## Touchscreen configuration

The touchscreen is wired to use the SPI1 interface of raspberry pi.

### Wiring

|Module|Raspberry Pi Zero W|
|---|---|
|T_IRQ|GPIO26|
|T_DO|SPI1-MOSI(pin 35)|
|T_DIN|SPI1-MISO(pin 38)|
|T_CS|GPIO23(pin 16, see dtoverlay spi1-1cs config)|
|T_CLK|pin 39|

### Configuration

There's a dtoverlay for XPT2046/ADS7846 touch screen interfaces, but it works with SPI0. To use SPI1 instead, you can add a custom overlay. Compile the following dtoverlay file, named 'ads7846-spi1-overlay.dts':

```
/*
 * Generic Device Tree overlay for the ADS7846 touch controller on SPI1
 *
 */

/dts-v1/;
/plugin/;

/ {
	compatible = "brcm,bcm2835", "brcm,bcm2708", "brcm,bcm2709";

	fragment@0 {
		target = <&gpio>;
		__overlay__ {
			ads7846_pins: ads7846_pins {
				brcm,pins = <255>; /* illegal default value */
				brcm,function = <0>; /* in */
				brcm,pull = <0>; /* none */
			};
		};
	};

	fragment@1 {
		target = <&spi1>;
		__overlay__ {
			/* needed to avoid dtc warning */
			#address-cells = <1>;
			#size-cells = <0>;

			ads7846: ads7846@0 {
				compatible = "ti,ads7846";
				reg = <0>;
				pinctrl-names = "default";
				pinctrl-0 = <&ads7846_pins>;

				spi-max-frequency = <2000000>;
				interrupts = <255 2>; /* high-to-low edge triggered */
				interrupt-parent = <&gpio>;
				pendown-gpio = <&gpio 255 0>;

				/* driver defaults */
				ti,x-min = /bits/ 16 <0>;
				ti,y-min = /bits/ 16 <0>;
				ti,x-max = /bits/ 16 <0x0FFF>;
				ti,y-max = /bits/ 16 <0x0FFF>;
				ti,pressure-min = /bits/ 16 <0>;
				ti,pressure-max = /bits/ 16 <0xFFFF>;
				ti,x-plate-ohms = /bits/ 16 <400>;
			};
		};
	};
	__overrides__ {
		cs =     <&ads7846>,"reg:0";
		speed =  <&ads7846>,"spi-max-frequency:0";
		penirq = <&ads7846_pins>,"brcm,pins:0", /* REQUIRED */
			 <&ads7846>,"interrupts:0",
			 <&ads7846>,"pendown-gpio:4";
		penirq_pull = <&ads7846_pins>,"brcm,pull:0";
		swapxy = <&ads7846>,"ti,swap-xy?";
		xmin =   <&ads7846>,"ti,x-min;0";
		ymin =   <&ads7846>,"ti,y-min;0";
		xmax =   <&ads7846>,"ti,x-max;0";
		ymax =   <&ads7846>,"ti,y-max;0";
		pmin =   <&ads7846>,"ti,pressure-min;0";
		pmax =   <&ads7846>,"ti,pressure-max;0";
		xohms =  <&ads7846>,"ti,x-plate-ohms;0";
	};
};
```

Compile it and copy it to /boot/overlays:

```
dtc -@ -I dts -O dtb -o ads7846-spi1.dtbo ads7846-spi1-overlay.dts
sudo cp ads7846-spi1.dtbo /boot/overlays
```

Open the /boot/config.txt file with a text editor and add the following two lines:

```
dtoverlay=spi1-1cs,cs0_pin=23,cs0_spidev=off
dtoverlay=ads7846-spi1,penirq=26,cs=1,speed=2000000,swapxy=1,xmin=230,xmax=3850,ymin=190,ymax=3850,pmax=255,xohms=100
```

The first line enables the SPI1 interface with one chip select pin. The chip select pin is set to GPIO23 (pin 16), because the default was already in the rpi-ibex configuration. The second line enables the custom ads7846 overlay that works with SPI1. The PENIRQ (T_IRQ) signal is configured to be GPIO26.

Reboot.

### Troubleshooting

To see the dtoverlay messages do:

```
sudo vcdbg log msg
```

If the touchscreen is properly configured, touch events will trigger an interrupt. The number of triggered interrupts on that line can be checked with:

```
# cat /proc/interrupts | grep ads7846
```

Some tools to calibrate the touchscreen:

```
xinput_calibration
```

To detect input events use ```evtest```.