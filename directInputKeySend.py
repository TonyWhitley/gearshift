# https://www.reddit.com/r/learnpython/comments/22tke1/use_python_to_send_keystrokes_to_games_in_windows/
# It works in rF2!

# DirectInput Key Code Table
#  Macro,           Value, # Symbol, Remarks
DirectInputKeyCodeTable = {
  'DIK_ESCAPE':     0x01, # Esc
  'DIK_1':          0x02, # 1
  'DIK_2':          0x03, # 2
  'DIK_3':          0x04, # 3
  'DIK_4':          0x05, # 4
  'DIK_5':          0x06, # 5
  'DIK_6':          0x07, # 6
  'DIK_7':          0x08, # 7
  'DIK_8':          0x09, # 8
  'DIK_9':          0x0A, # 9
  'DIK_0':          0x0B, # 0
  'DIK_MINUS':      0x0C, # -
  'DIK_EQUALS':     0x0D, # =
  'DIK_BACK':       0x0E, # Back Space
  'DIK_TAB':        0x0F, # Tab
  'DIK_Q':          0x10, # Q
  'DIK_W':          0x11, # W
  'DIK_E':          0x12, # E
  'DIK_R':          0x13, # R
  'DIK_T':          0x14, # T
  'DIK_Y':          0x15, # Y
  'DIK_U':          0x16, # U
  'DIK_I':          0x17, # I
  'DIK_O':          0x18, # O
  'DIK_P':          0x19, # P
  'DIK_LBRACKET':   0x1A, # [
  'DIK_RBRACKET':   0x1B, # ]
  'DIK_RETURN':     0x1C, # Enter
  'DIK_LContol':    0x1D, # Ctrl (Left)
  'DIK_A':          0x1E, # A
  'DIK_S':          0x1F, # S
  'DIK_D':          0x20, # D
  'DIK_F':          0x21, # F
  'DIK_G':          0x22, # G
  'DIK_H':          0x23, # H
  'DIK_J':          0x24, # J
  'DIK_K':          0x25, # K
  'DIK_L':          0x26, # L
  'DIK_SEMICOLON':  0x27, # ;
  'DIK_APOSTROPHE': 0x28, # 
  'DIK_GRAVE':      0x29, # `
  'DIK_LSHIFT':     0x2A, # Shift (Left)
  'DIK_BACKSLASH':  0x2B, # \
  'DIK_Z':          0x2C, # Z
  'DIK_X':          0x2D, # X
  'DIK_C':          0x2E, # C
  'DIK_V':          0x2F, # V
  'DIK_B':          0x30, # B
  'DIK_N':          0x31, # N
  'DIK_M':          0x32, # M
  'DIK_COMMA':      0x33, # ", # "
  'DIK_PERIOD':     0x34, # .
  'DIK_SLASH':      0x35, # /
  'DIK_RSHIFT':     0x36, # Shift (Right)
  'DIK_MULTIPLY':   0x37, # * (Numpad)
  'DIK_LMENU':      0x38, # Alt (Left)
  'DIK_SPACE':      0x39, # Space
  'DIK_CAPITAL':    0x3A, # Caps Lock
  'DIK_F1':         0x3B, # F1
  'DIK_F2':         0x3C, # F2
  'DIK_F3':         0x3D, # F3
  'DIK_F4':         0x3E, # F4
  'DIK_F5':         0x3F, # F5
  'DIK_F6':         0x40, # F6
  'DIK_F7':         0x41, # F7
  'DIK_F8':         0x42, # F8
  'DIK_F9':         0x43, # F9
  'DIK_F10':        0x44, # F10
  'DIK_NUMLOCK':    0x45, # Num Lock
  'DIK_SCROLL':     0x46, # Scroll Lock
  'DIK_NUMPAD7':    0x47, # 7 (Numpad)
  'DIK_NUMPAD8':    0x48, # 8 (Numpad)
  'DIK_NUMPAD9':    0x49, # 9 (Numpad)
  'DIK_SUBTRACT':   0x4A, # - (Numpad)
  'DIK_NUMPAD4':    0x4B, # 4 (Numpad)
  'DIK_NUMPAD5':    0x4C, # 5 (Numpad)
  'DIK_NUMPAD6':    0x4D, # 6 (Numpad)
  'DIK_ADD':        0x4E, # + (Numpad)
  'DIK_NUMPAD1':    0x4F, # 1 (Numpad)
  'DIK_NUMPAD2':    0x50, # 2 (Numpad)
  'DIK_NUMPAD3':    0x51, # 3 (Numpad)
  'DIK_NUMPAD0':    0x52, # 0 (Numpad)
  'DIK_DECIMAL':    0x53, # . (Numpad)
  'DIK_F11':        0x57, # F11
  'DIK_F12':        0x58, # F12
  'DIK_F13':        0x64, # F13, # NEC PC-98
  'DIK_F14':        0x65, # F14, # NEC PC-98
  'DIK_F15':        0x66, # F15, # NEC PC-98
  'DIK_KANA':       0x70, # Kana, # Japanese Keyboard
  'DIK_CONVERT':    0x79, # Convert, # Japanese Keyboard
  'DIK_NOCONVERT':  0x7B, # No Convert, # Japanese Keyboard
  'DIK_YEN':        0x7D, # ¥, # Japanese Keyboard
  'DIK_NUMPADEQUALS': 0x8D, # =, # NEC PC-98
  'DIK_CIRCUMFLEX': 0x90, # ^, # Japanese Keyboard
  'DIK_AT':         0x91, # @, # NEC PC-98
  'DIK_COLON':      0x92, # :          , # NEC PC-98
  'DIK_UNDERLINE':  0x93, # _, # NEC PC-98
  'DIK_KANJI':      0x94, # Kanji, # Japanese Keyboard
  'DIK_STOP':       0x95, # Stop, # NEC PC-98
  'DIK_AX':         0x96, # (Japan AX)
  'DIK_UNLABELED':  0x97, # (J3100)
  'DIK_NUMPADENTER':0x9C, # Enter (Numpad)
  'DIK_RCONTROL':   0x9D, # Ctrl (Right)
  'DIK_NUMPADCOMMA':0xB3, # ", #  (Numpad)", # NEC PC-98
  'DIK_DIVIDE':     0xB5, # / (Numpad)
  'DIK_SYSRQ':      0xB7, # Sys Rq
  'DIK_RMENU':      0xB8, # Alt (Right)
  'DIK_PAUSE':      0xC5, # Pause
  'DIK_HOME':       0xC7, # Home
  'DIK_UP':         0xC8, # Cursor up
  'DIK_PRIOR':      0xC9, # Page Up
  'DIK_LEFT':       0xCB, # Cursor left
  'DIK_RIGHT':      0xCD, # Cursor right
  'DIK_END':        0xCF, # End
  'DIK_DOWN':       0xD0, # Cursor down
  'DIK_NEXT':       0xD1, # Page Down
  'DIK_INSERT':     0xD2, # Insert
  'DIK_DELETE':     0xD3, # Delete
  'DIK_LWIN':       0xDB, # Windows
  'DIK_RWIN':       0xDC, # Windows
  'DIK_APPS':       0xDD, # Menu
  'DIK_POWER':      0xDE, # Power
  'DIK_SLEEP':      0xDF, # Windows
  }

import ctypes, time
# Bunch of stuff so that the script can send keystrokes to game #

SendInput = ctypes.windll.user32.SendInput

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

# Actual Functions

def PressKey(keyStr):
  ###########################################
  # debug
  #print(keyStr)
  #return True
  ###########################################
  try:
    hexKeyCode = DirectInputKeyCodeTable[keyStr]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    return True
  except:
    return False

def ReleaseKey(keyStr):
  try:
    hexKeyCode = DirectInputKeyCodeTable[keyStr]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    return True
  except:
    return False

if __name__ == "__main__":
    time.sleep(3)
    PressKey('DIK_Q')   # press Q
    time.sleep(.05)
    ReleaseKey('DIK_Q') # release Q
