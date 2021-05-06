# https://github.com/ryansalerno/raspberry-pico-retro-controller-adapters

import digitalio
import usb_hid
from adafruit_hid.gamepad import Gamepad
from time import sleep
import board

# some data pins are shared and change meaning based on the <select> modifier
genesis_buttons = {0: 'up', 1: 'down', 2: 'left',
                   3: 'right', 4: 'b', 5: 'c', 6: 'a', 7: 'start'}
pressed = {}
# generic gamepad button mappings (see: https://gamepad-tester.com/)
gamepad_buttons = {'up': 13, 'down': 14, 'left': 15,
                   'right': 16, 'a': 3, 'start': 10, 'b': 1, 'c': 2}

# the Genesis controller looks like this:
#
# -------------      1. Up       5. Power
# \ 1 2 3 4 5 /      2. Down     6. A / B
#  \ 6 7 8 9 /       3. Left     7. <Select>
#   ---------        4. Right    8. Ground
#                                9. Start / C

# and you want to wire it up like this:
#
# Genesis        Pico
# --------------------
# 1 Up           GP2
# 2 Down         GP3
# 3 Left         GP4
# 4 Right        GP5
# 6 A / B        GP6
# 9 Start / C    GP7
# 7 <Select>     GP22
# 5 Power        3V3
# 8 Ground       GND (any)

gamepad = Gamepad(usb_hid.devices)

up = digitalio.DigitalInOut(board.GP2)
down = digitalio.DigitalInOut(board.GP3)
left = digitalio.DigitalInOut(board.GP4)
right = digitalio.DigitalInOut(board.GP5)
ab = digitalio.DigitalInOut(board.GP6)
c = digitalio.DigitalInOut(board.GP7)

data = [up, down, left, right, ab, c]
buttons = len(data)
for pin in data:
	pin.direction = digitalio.Direction.INPUT
	pin.pull = digitalio.Pull.UP

select = digitalio.DigitalInOut(board.GP22)
select.direction = digitalio.Direction.OUTPUT

wait = .00001

while True:
	select.value = True
	sleep(wait)
	for h, btn in enumerate(data):
		pressed[h] = data[h].value

	select.value = False
	sleep(wait)
	pressed[buttons] = ab.value
	pressed[buttons+1] = c.value

	# and since we know the state of all buttons, let's press 'em
	for index in pressed:
		# Data pulls up (grounds when pressed), which means we actually press on False
		if pressed[index] == True:
			gamepad.release_buttons(gamepad_buttons[genesis_buttons[index]])
		else:
			gamepad.press_buttons(gamepad_buttons[genesis_buttons[index]])
