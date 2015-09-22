import re

import win32gui
import win32con

import WindowsTools
import WindowsTools.Defines

def _send_key(key, HWND):
	win32gui.SendMessage(HWND, win32con.WM_KEYDOWN, key, WindowsTools.Defines.LPARAM)
	win32gui.SendMessage(HWND, win32con.WM_CHAR, key, WindowsTools.Defines.LPARAM)
	win32gui.SendMessage(HWND, win32con.WM_KEYUP, key, LPARAM_UP)

def send_key(key, HWND, send_to_children=False):
	"""Send a simulated keypress to a window.

	Keyword arguments:
	key -- ID of the key you want to send (decimal)
	HWND -- The window handle of the target window
	send_to_children -- if True, the keypress will be sent to all child-windows of the parent

	"""
	_send_key(key, HWND)
	if send_to_children:
		child_windows = WindowsTools.enum_child_windows(HWND)
		for window in child_windows:
			_send_key(key, window)

def send_key_to_windows_with_title(key, regex, send_to_children=False):
	"""Send a simulated keypress to all windows with titles matching a regular expression

	Keyword arguments:
	key -- ID of the key you want to send (decimal)
	regex -- The regular expression to search with
	send_to_children -- if True, the keypress will be sent to all child-windows of the parent

	"""
	windows = WindowsTools.enum_windows(regex)
	for HWND in windows:
		_send_key(key, HWND)
		if send_to_children:
			child_windows = WindowsTools.enum_child_windows(window)
			for window in child_windows:
				_send_key(key, window)