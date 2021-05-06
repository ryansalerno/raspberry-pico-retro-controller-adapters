# Raspberry Pico Retro Controller Adapters

The go-to DIY adapters are Arduino-based (see: [DaemonBite](https://github.com/MickGyver/DaemonBite-Retro-Controllers-USB) and/or [the MiSTer fork of them](https://github.com/MiSTer-devel/Retro-Controllers-USB-MiSTer)). I wanted to see what a $4 Pico could do instead....

-----

Apparently the CircuitPython HID libraries are more mature and performant than MicroPython at the moment. It's also really easy and delightful to use. Maybe someone will be motivated to port the Arduino code to work with the [Pico's SDK](https://github.com/raspberrypi/pico-sdk) (or maybe it already works and I was just too afraid to try to compile?). But either way, these scripts work great and are easily modified if you want to add some wacky macros or extra stuff.

The original code was adapted from: https://github.com/printnplay/Pico-MicroPython/blob/main/NES2USB.py

## Getting Started

Grab the Pico UF2 image from here: https://circuitpython.org/board/raspberry_pi_pico/

And we also rely on CircuitPython's `hid` library you can snag here: https://circuitpython.org/libraries

1. connect the wires from a controller (or, preferably, an extension cable) to the Pico according to the notes in the relevant script.
2. plug in your Pico while holding the `bootsel` button
3. drag the UF2 image onto the root of your mounted Pico
4. the pico will reboot and remount and you'll see a `lib` folder
5. drag the `adafruit_hid` folder from the extracted library collection into the Pico's `lib` folder
6. copy the relevant script from this repo into the Pico's pre-existing `code.py`

### Live Debugging:

https://learn.adafruit.com/welcome-to-circuitpython/interacting-with-the-serial-console

## Latency

I don't have [reputable numbers](https://inputlag.science/controller/methodology) for you (if you want to contribute some tests, please open an issue and I'll update this section!). Anecdotally, I can tell you I'm picky and found the SNES Classic to be much too slow feeling, and these perform as well as the [recommended](https://github.com/MiSTer-devel/Main_MiSTer/wiki/Selecting-Input-Devices#what-is-the-fastest-usb-controller-i-can-get) USB DualShock4 plugged into my MiSTer.