import win32api, win32con

def set_cursor_pos(x, y):
    # x, y in 0, 1
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
        int(x * 65535.0),
        int(y * 65535.0))

def get_cursor_pos():
    width, height = win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    x_raw, y_raw = win32api.GetCursorPos()
    return x_raw/width, y_raw/height

# See https://gist.github.com/chriskiehl/2906125 for keycodes

KEY_CODE = 0x4A  # "J" key

def send_keydown():
    win32api.keybd_event(KEY_CODE, 0, 0, 0)

def send_keyup():
    win32api.keybd_event(KEY_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)

