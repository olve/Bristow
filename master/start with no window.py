import WindowsTools
from os import path
python_path = path.normpath("R:\\python27\\python.exe")
bristow_path = path.normpath("C:\\xqoBase\\Bristow\\Bristow.py")

WindowsTools.create_process(python_path, bristow_path)