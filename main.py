import win32api, win32con, win32clipboard
import time
import ctypes


#First let's define the positions of the buttons
list_positions = [
	(1069, 400),
	(1069, 510),
	(1069, 628),
	(1069, 741),
	(1069, 845),
	(1069, 400)]

#Then generating the inputs -------------------------------------------
SendInput = ctypes.windll.user32.SendInput


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def copy():
    PressKey(0x11) #Ctrl
    PressKey(0x41) #C
    ReleaseKey(0x41) #~C
    ReleaseKey(0x11) #~Ctrl
    PressKey(0x11) #Ctrl
    PressKey(0x43) #C
    ReleaseKey(0x43) #~C
    ReleaseKey(0x11) #~Ctrl

#if __name__ =="__main__":
#	click(10, 10)
#	time.sleep(1)
#	run()
#-------------------------------------------------------------------------------

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def previousPage():
	click(20,53)

def setup():
	#focus page
	click(10, 10)
	#click first
	click(1067, 625)
	#wait loading
	time.sleep(2)
	previousPage()
	#all set

def getFromClipBoard():
	win32clipboard.OpenClipboard()
	data = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()
	return data

setup()
click(10, 10)
time.sleep(2)
count = 0
getFromClipBoard()
for x, y in list_positions:
	
	click(x,y)
	time.sleep(2)

	copy()
	print(count)
	data = getFromClipBoard()

	file_name = "datas/novembre/file"+str(count)
	count+=1
	file = open(file_name, "w") 
	file.write(data)
	file.close() 

	previousPage()
	time.sleep(2)