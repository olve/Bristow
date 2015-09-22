import pythoncom

import pyHook

def bind_keys(keybindings):
	"""Listens for keystrokes and runs instructions bound to keystrokes in keybindings

	Keyword arguments:
	keybindings -- a dictionary containing key-names and the instructions they are bound to
	key-names are defined in pyHook

	Example: keybindings = {"numpad0":MyClass.myFunc(arg1,arg2)}

	"""
	def _on_keyboard_event(event):
		key_name = event.Key
		if key_name in keybindings:
			keybindings[key_name]()
			# Returning False blocks the original keypress-message from being passed to the foreground window
			return False
		else:
			return True
	hook_manager = pyHook.HookManager()
	hook_manager.KeyDown = _on_keyboard_event
	hook_manager.HookKeyboard()
	pythoncom.PumpMessages()