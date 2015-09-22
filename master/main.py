# This is the main script, append your own instructions and keybindings here.
# Known Bugs:
# 	get_pid_from_HWND returns 0 on very rare occasions, with certain programs.
#	GetLastError returns 0x6 which is Invalid Handle, but HWNDs seem to be as they should
#
#	SpotifyController wont work when spotify is run as administrator

import threading

import KeyboardHook
import SpotifyControls
import WindowsTools
import WindowsTools.SendKey

def create_thread(function, arguments=None):
	"""Runs function in its own thread. arguments must be a tuple"""
	if arguments is not None:
		thread = threading.Thread(target=function, args=arguments)
	else:
		thread = threading.Thread(target=function)
	thread.start()

#Hook Spotify and start controller
spotify_hook = SpotifyControls.SpotifyHook()
create_thread(spotify_hook.start_hook)

# Keybindings for KeyboardHook
# Keybinding-format: "key-name":lambda : instruction(arg1, arg2)
keybindings = {
								"Numpad1":lambda : spotify_hook.controller.previous_track(),
								"Numpad3":lambda : spotify_hook.controller.next_track(),
								"Multiply":lambda : spotify_hook.controller.playpause(),
								"Add":lambda : spotify_hook.controller.volume_up(),
								"Subtract":lambda : spotify_hook.controller.volume_down(),
								"Numpad0":lambda : WindowsTools.SendKey.send_key_to_windows_with_title(32, regex="VLC media player"),
								"Decimal":lambda : WindowsTools.SendKey.send_key_to_windows_with_title(70, regex="VLC media player"),
								#"Numpad4":lambda : WindowsFunctions.kill_window_process(regex="Fallout3"),
								"Numpad7":lambda : WindowsTools.kill_process_by_HWND(WindowsTools.get_foreground_window()),
								"Numpad8":lambda : SpotifyControls.restart_spotify("C:/Users/xqo/AppData/Roaming/Spotify/spotify.exe"),
								#"Numpad5":lambda : ChromeFunctions.playpause_youtube(),
								#"Numpad5":lambda : LoadExe.load("calc.exe"),
}

# Hook keyboard
create_thread(KeyboardHook.bind_keys, arguments=(keybindings,))