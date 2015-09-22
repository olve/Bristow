import ctypes
import re

import win32gui

import Defines

def open_process(pid, access_right=Defines.PROCESS_ALL_ACCESS):
	"""Returns a handle to an open process

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms684320(v=vs.85).aspx

	"""
	kernel32 = ctypes.windll.kernel32
	process_handle = kernel32.OpenProcess(access_right, False, pid)
	return process_handle

def get_pid_from_HWND(HWND):
	"""Returns the process-id of the process associated with a window handle

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms633522(v=vs.85).aspx

	"""
	user32 = ctypes.windll.user32
	output = Defines.DWORD()
	user32.GetWindowThreadProcessId(HWND, ctypes.byref(output))
	pid = output.value
	return pid

def wait_for_single_object(process_handle):
	"""Hooks a process or thread referenced by a handle to the open object, and returns when the process has died

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms687032(v=vs.85).aspx

	"""
	kernel32 = ctypes.windll.kernel32
	kernel32.WaitForSingleObject(process_handle, Defines.INFINITY)
	return True

def hook_process_by_pid(pid):
	"""Hooks a process referenced by process-id and returns when the process dies

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms687032(v=vs.85).aspx

	"""
	process_handle = open_process(pid)
	wait_for_single_object(process_handle)

def hook_process_by_hwnd(HWND):
	"""Hooks a process referenced by a handle to the window the process belongs to and returns when the process dies"""
	pid = get_pid_from_HWND(HWND)
	hook_process_by_pid(pid)

def kill_process(pid, exit_code=-1):
	"""Terminates a process referenced by its process-id

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms686714(v=vs.85).aspx

	"""
	kernel32 = ctypes.windll.kernel32
	process_handle = open_process(pid, Defines.PROCESS_TERMINATE)
	kernel32.TerminateProcess(process_handle, exit_code)

def kill_process_by_HWND(HWND):
	"""Kills the process associated with the window"""
	pid = get_pid_from_HWND(HWND)
	kill_process(pid)

def kill_processes_with_title(regex):
	"""Kills processes associated with top-level windows that have titles matching a regular expression"""
	matching_windows = enum_windows(regex)
	for HWND in matching_windows:
		kill_process_by_HWND(HWND)

def enum_windows(regex=None):
	"""Enumerate all top-level windows

	Keyword arguments:
	regex -- If not None, only return windows with a title matching the regular expression

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms633497(v=vs.85).aspx

	"""
	toplevel_windows = {}
	def callback(*window_info):
		HWND = window_info[0]
		title = win32gui.GetWindowText(HWND)
		if regex is not None:
			if re.findall(regex, title):
				toplevel_windows[HWND] = title
		else:
			toplevel_windows[HWND] = title
	win32gui.EnumWindows(callback, 0)
	return toplevel_windows

def get_foreground_window():
	"""Retrieves a handle to the foreground window (the window with which the user is currently interacting).

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms633505(v=vs.85).aspx

	"""
	user32 = ctypes.windll.user32
	return user32.GetForegroundWindow()

def find_window(class_name=None, window_title=None):
	"""Returns the HWND of a window, can search by window-title and/or window class-name.

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms633499(v=vs.85).aspx

	"""
	return win32gui.FindWindow(class_name, window_title)

def enum_child_windows(parent_window_HWND):
	"""Enumerate all child windows of a window referenced by HWND

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms633494(v=vs.85).aspx

	"""
	child_windows = []
	def callback(*child_window):
		child_windows.append(child_window[0])
	wi32gui.EnumChildWindows(parent_window, callback, "Enumerating")
	return child_windows

def create_process(path_to_exe, arguments=None, creation_flags=Defines.CREATE_NO_WINDOW):
	"""Launches an executable

	Keyword arguments:
	path_to_exe --- path to the executable to start
	arguments -- whatever args you want to supply, must be a string
	creation_flags -- Flags that control how the executable is started. Defines.CREATE_NO_WINDOW launches the executable without creating a window, Defines.CREATE_NEW_CONSOLE launches
	the executable and creates windows (Default: Defines.CREATE_NO_WINDOW)

	http://msdn.microsoft.com/en-us/library/windows/desktop/ms682425(v=vs.85).aspx

	"""
	kernel32 = ctypes.windll.kernel32
	if arguments:
		lpCommandLine = "%s %s" % (path_to_exe, arguments)
	else:
		lpCommandLine = None
	startupinfo = Defines.STARTUPINFO()
	process_information = Defines.PROCESS_INFORMATION()
	startupinfo.dwFlags = 0x1
	startupinfo.wShowWindow = 0x0
	startupinfo.cb = ctypes.sizeof(startupinfo)
	if kernel32.CreateProcessA(path_to_exe, lpCommandLine, None, None, None, creation_flags, None, None, ctypes.byref(startupinfo), ctypes.byref(process_information)):
		return None
	else:
		return "Error: 0x%08x" % kernel32.GetLastError()