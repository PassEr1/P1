import ctypes
def get_windows():
        """
        Return a list which contains the opened windows titles.
        :return: title (list)
        """

        EnumWindows = ctypes.windll.user32.EnumWindows  # Filters all toplevel(opened) windows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int),
                                             ctypes.POINTER(ctypes.c_int))  # Callback function. Returns a tuple
        GetWindowText = ctypes.windll.user32.GetWindowTextW  # Gets window's title
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW  # Gets the exacly buffer size of the title
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible  # Filters all the visible windows

        titles = []

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                titles.append(buff.value)
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)  # Callback
        return titles

#for i in get_windows():
 #   print i
import os
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    print str(f)