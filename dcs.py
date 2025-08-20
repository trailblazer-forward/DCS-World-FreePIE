# For DCS World
from ctypes import windll
from time import sleep
from collections import namedtuple

set_mouse = windll.user32.SetCursorPos  # Function to set mouse's pos
WINDOW_X = 2880
WINDOW_Y = 1800

def clamp(value, minv, maxv):
	"""
	This function will return the parameter value if the parameter lies within the range of values between the minimum and maximum values.

	If the parameter is greater than the range, the function will return the maximum value.
	
	If the argument is less than the range, the function will return the minimum value.
	"""
	return max(min(value, maxv), minv)


def checked_add(num, add, max_v, min_v):
	"""
	return num + add if not overflowing, otherwise the maximum/minimum value
	"""
	return clamp(num + add, min_v, max_v)

def mouse_to_middle():
	"""
	set middle to the middle of the screen
	"""
	set_mouse(WINDOW_X / 2, WINDOW_Y / 2)

def add(x, y):
	return checked_add(x, y, vJoy[0].axisMax, -vJoy[0].axisMax)

def handle_sliders_active():
	"""
	Handling throttle activation
	"""
	is_active['slider1'] = is_active['slider2'] = is_active['mouse']
	if keyboard.getKeyDown(Key.RightAlt):
		is_active['slider1'] = True
	if keyboard.getKeyDown(Key.RightControl):
		is_active['slider2'] = True
	if keyboard.getKeyDown(Key.RightShift):
		is_active['slider1'] = is_active['slider2'] = True
	
def handle_wheel():
	"""
	Handling middle mouse button scrolling
	"""
	if mouse.wheelUp:
		flag = -1
	elif mouse.wheelDown:
		flag = 1
	else:
		if keyboard.getPressed(Key.Delete):
			vJoy[0].slider = vJoy[0].dial = max(vJoy[0].slider, vJoy[0].dial)
		return
	if is_active['slider1']:
		vJoy[0].slider = add(vJoy[0].slider, flag * sensitive['slider1'])
	if is_active['slider2']:
		vJoy[0].dial = add(vJoy[0].dial, flag * sensitive['slider2'])
	
def handle_mouse():
	"""
	handle mouse movements
	"""
	vJoy[0].x = add(vJoy[0].x, sensitive['mouse_x'] * mouse.deltaX)
	vJoy[0].y = add(vJoy[0].y, sensitive['mouse_y'] * mouse.deltaY)
	if mouse.getPressed(2):
		vJoy[0].x = vJoy[0].y = 0
	vJoy[0].setButton(0, mouse.getButton(0))
	vJoy[0].setButton(1, mouse.getButton(1))
	mouse_to_middle()
	
def update():
	if keyboard.getPressed(Key.Insert):
		is_active['mouse'] = not is_active['mouse']
		if is_active['mouse']:
			mouse_to_middle()
			handle_mouse()
			vJoy[0].x = vJoy[0].y = 0
	elif is_active['mouse']:
		handle_mouse()
	handle_sliders_active()
	handle_wheel()

if starting:  # initalize
	axis = {'x': 0, 'y': 0}
	sensitive = {'mouse_x': 7.5, 'mouse_y': 7.5, 'slider1': 500.0, 'slider2': 500.0}
	is_active = {'mouse': False, 'slider1': False, 'slider2': False}
	vJoy[0].slider = vJoy[0].dial = vJoy[0].axisMax

update()