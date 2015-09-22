import ctypes

## Microsoft Types
DWORD = ctypes.c_ulong
LPBYTE = ctypes.POINTER(ctypes.c_ubyte)
LPTSTR = ctypes.POINTER(ctypes.c_char)
HANDLE = ctypes.c_void_p
WORD = ctypes.c_ushort

CREATE_NO_WINDOW = 0x08000000
CREATE_NEW_CONSOLE = 0x00000010
PROCESS_ALL_ACCESS = 0x001F0FFF
PROCESS_TERMINATE = 0x00000001

INFINITY = 0xFFFFFFFF

#LONG PARAMETERs for SendMessage
LPARAM = 0x220001
LPARAM_UP = 0xC0220001

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb",            DWORD),        
        ("lpReserved",    LPTSTR), 
        ("lpDesktop",     LPTSTR),  
        ("lpTitle",       LPTSTR),
        ("dwX",           DWORD),
        ("dwY",           DWORD),
        ("dwXSize",       DWORD),
        ("dwYSize",       DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute",DWORD),
        ("dwFlags",       DWORD),
        ("wShowWindow",   WORD),
        ("cbReserved2",   WORD),
        ("lpReserved2",   LPBYTE),
        ("hStdInput",     HANDLE),
        ("hStdOutput",    HANDLE),
        ("hStdError",     HANDLE),
        ]
class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess",    HANDLE),
        ("hThread",     HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId",  DWORD),
        ]