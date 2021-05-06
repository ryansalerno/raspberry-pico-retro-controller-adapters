# https://github.com/ryansalerno/raspberry-pico-retro-controller-adapters
# indispensible primer on what's happening and why: https://www.youtube.com/watch?v=dahbvSYV0KA

import digitalio
import usb_hid
from adafruit_hid.gamepad import Gamepad
from time import sleep
import board

# NES controller sends the state of each button in this order
nes_buttons = {0: 'a', 1: 'b', 2: 'select',
               3: 'start', 4: 'up', 5: 'down', 6: 'left', 7: 'right'}
pressed = {}
# generic gamepad button mappings (see: https://gamepad-tester.com/)
gamepad_buttons = {'up': 13, 'down': 14, 'left': 15,
                   'right': 16, 'select': 9, 'start': 10, 'a': 2, 'b': 1}

# the NES controller looks like this:
#
#  ---\        1: Ground
# | 1  \       2: Clock
# | 2 5 |      3: Latch
# | 3 6 |      4: Data
# | 4 7 |      5: VCC
#  -----

# and you want to wire it up like this:
#
# NES          Pico
# ------------------
# Ground       GND (any)
# Clock        GP4
# Latch        GP5
# Data         GP6
# VCC          3V3

gamepad = Gamepad(usb_hid.devices)

clock = digitalio.DigitalInOut(board.GP4)
latch = digitalio.DigitalInOut(board.GP5)
data = digitalio.DigitalInOut(board.GP6)

latch.direction = digitalio.Direction.OUTPUT
clock.direction = digitalio.Direction.OUTPUT
data.direction = digitalio.Direction.INPUT

data.pull = digitalio.Pull.UP

latch.value = False
clock.value = False

# these are the SNES timings, and apparently NES can be made to run much faster between cycles, buuuuut....
cycle_latch = 0.000012  # 12µs according to spec
cycle_clock = 0.000006  # 6µs according to spec
cycle_pause = 0.000006  # 6µs according to spec

while True:
	# toggle the latch to indicate we're polling for current button states
	latch.value = True
	sleep(cycle_latch)
	latch.value = False
	sleep(cycle_pause)

	# the A button is always sent immediately
	pressed[0] = data.value

	# now cycle through the rest of the buttons in order
	for x in range(1, 8):
		# each clock pulse tells the controller to send the next button in its internal order
		clock.value = True
		sleep(cycle_clock)
		clock.value = False
		sleep(cycle_pause)

		pressed[x] = data.value

	# and since we know the state of all buttons, let's press 'em
	for index in pressed:
		# Data pulls up (grounds when pressed), which means we actually press on False
		if pressed[index] == True:
			gamepad.release_buttons(gamepad_buttons[nes_buttons[index]])
		else:
			gamepad.press_buttons(gamepad_buttons[nes_buttons[index]])
