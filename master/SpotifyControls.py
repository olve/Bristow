import threading
import time

import pytify

import WindowsTools
import WindowsTools.Defines

def get_spotify_instance():
	"""Get instance of the currently running Spotify"""
	spotify = pytify.Spotify()
	return spotify

def restart_spotify(spotify_exe_path):
	"""Terminates and restarts spotify"""
	spotify_hwnd = get_spotify_instance()._hwnd
	WindowsTools.kill_process_by_HWND(spotify_hwnd)
	WindowsTools.create_process(spotify_exe_path, creation_flags=WindowsTools.Defines.CREATE_NEW_CONSOLE)

class Control(object):
	"""Controls Spotify playback"""
	def __init__(self, spotify):
		self.spotify = spotify
	def previous_track(self):
		self.spotify.previous()
	def next_track(self):
		self.spotify.next()
	def playpause(self):
		self.spotify.playpause()
	def volume_up(self):
		for i in xrange(1,3):
			self.spotify.volumeUp()
	def volume_down(self):
		for i in xrange(1,3):
			self.spotify.volumeDown()

class SpotifyHook(object):
	"""Finds and hooks the running Spotify-process until it dies. Finds and hooks it again if it restarts"""
	def __init__(self):
		spotify = get_spotify_instance()
		self.controller = Control(spotify)
	def start_hook(self):
		while True:
			spotify = get_spotify_instance()
			# HWND is a handle to an open window in Windows.
			HWND = spotify._hwnd
			self.controller = Control(spotify)
			# Only try to hook Spotify if it is actually running.
			if HWND is not 0:
				thread = threading.Thread(target=WindowsTools.hook_process_by_hwnd, args=(HWND,))
				thread.start()
				# loop pauses here until WindowsTools.hook_process_by_hwnd returns, ie when the spotify-process dies
				thread.join()
			# Wait 1 second inbetween scans for spotify to reduce CPU load
			time.sleep(1)