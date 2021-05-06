# https://github.com/ryansalerno/raspberry-pico-retro-controller-adapters
# indispensible primer on what's happening and why (NES): https://www.youtube.com/watch?v=dahbvSYV0KA
# the SNES controller does everything the same, but with more buttons: https://gamefaqs.gamespot.com/snes/916396-super-nintendo/faqs/5395

import digitalio
import usb_hid
from adafruit_hid.gamepad import Gamepad
from time import sleep
import board

# SNES controller sends the state of each button in this order
snes_buttons = {0: 'b', 1: 'y', 2: 'select', 3: 'start', 4: 'up',
                5: 'down', 6: 'left', 7: 'right', 8: 'a', 9: 'x', 10: 'l', 11: 'r'}
button_count = len(snes_buttons)
pressed = {}
# generic gamepad button mappings (see: https://gamepad-tester.com/)
gamepad_buttons = {'up': 13, 'down': 14, 'left': 15, 'right': 16,
                   'select': 9, 'start': 10, 'a': 2, 'b': 1, 'x': 4, 'y': 3, 'l': 5, 'r': 6}

# the SNES controller looks like this:
#
#  -----------------        1: VCC       4: Data
# | 1 2 3 4 | 5 6 7 )       2: Clock     7: Ground
#  -----------------        3: Latch

# and you want to wire it up like this:
#
# SNES         Pico
# ------------------
# 7 Ground     GND (any)
# 2 Clock      GP4
# 3 Latch      GP5
# 4 Data       GP6
# 1 VCC        3V3

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

# hyper-specific timings taken from: https://github.com/MickGyver/DaemonBite-Retro-Controllers-USB/blob/master/SNESControllersUSB/SNESControllersUSB.ino
cycle_latch = 0.000012  # 12µs according to spec
cycle_clock = 0.000006  # 6µs according to spec
cycle_pause = 0.000006  # 6µs according to spec

while True:
	# toggle the latch to indicate we're polling for current button states
	latch.value = True
	sleep(cycle_latch)
	latch.value = False
	sleep(cycle_pause)

	# the B button is always sent immediately
	pressed[0] = data.value

	# now cycle through the rest of the buttons in order (the SNES expects 16 cycles, even though 13 - 16 are unused)
	for x in range(1, 16):
		# each clock pulse tells the controller to send the next button in its internal order
		clock.value = True
		sleep(cycle_clock)
		clock.value = False
		sleep(cycle_pause)

		if x < button_count:
			pressed[x] = data.value

	# and since we know the state of all buttons, let's press 'em
	for index in pressed:
		# Data pulls up (grounds when pressed), which means we actually press on False
		if pressed[index] == True:
			gamepad.release_buttons(gamepad_buttons[snes_buttons[index]])
		else:
			gamepad.press_buttons(gamepad_buttons[snes_buttons[index]])
