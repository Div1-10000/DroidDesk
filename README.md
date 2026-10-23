# DroidDesk — PC-to-Android Control Center

A Windows desktop app built with Python + PySide6 that uses Android Debug Bridge (ADB) for authorized Android device discovery, device information, app listing/launch, screenshots, and file transfers. It can launch **scrcpy** for interactive screen mirroring and control.

> DroidDesk is a local controller, not a stealth or unattended access tool. Enable Android Developer options / USB debugging yourself and approve the computer on the phone. Wireless debugging should only be enabled on trusted networks.

## Features

- USB device detection and ADB Wi-Fi device support
- Device model, Android version, battery level/status, storage summary
- Launch and stop scrcpy screen mirroring
- List installed third-party packages and launch selected apps
- Browse shared storage folders and upload/download files
- Take screenshots to a chosen PC path
- Dark dashboard UI with status and command output
- SQLite connection/event history
- ADB executable discovery from PATH or common Windows locations

## Requirements

- Windows 10/11
- Python 3.10+ (Python 3.12 recommended)
- Android phone with USB debugging enabled, or Android Wireless debugging paired
- Android Platform Tools (`adb`)
- scrcpy (for live mirroring/control)

Official downloads:
- ADB / Platform Tools: https://developer.android.com/tools/releases/platform-tools
- scrcpy: https://github.com/Genymobile/scrcpy
- Python: https://www.python.org/downloads/windows/

## Setup

1. Extract the ZIP to a normal folder, e.g. `C:\\Users\\YourName\\DroidDesk`.
2. Install Python and ensure `python` works in PowerShell.
3. Install Android Platform Tools and scrcpy. Add their folders to PATH, or set their paths under **Settings** in DroidDesk.
4. Open PowerShell in the extracted folder:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, use:

```powershell
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe main.py
```

## Quick start on Windows

After extracting the ZIP, double-click `Start-DroidDesk.bat`. It creates a local virtual environment, installs the Python dependency, and launches the app. An internet connection is needed the first time to install PySide6. Android Platform Tools (`adb.exe`) and `scrcpy.exe` are separate tools; install them or configure their paths in Settings.

## Connect over USB

1. On Android, open Settings → About phone and tap Build number as instructed by the device until Developer options are enabled.
2. Open Developer options → USB debugging.
3. Connect a data-capable USB cable, unlock the phone and approve the RSA prompt.
4. In DroidDesk, click **Refresh devices** and select the device.

Verify separately in PowerShell with `adb devices`. A device should be listed as `device`, not `unauthorized`.

## Connect over Wi-Fi

For Android 11+, enable Developer options → Wireless debugging. Use **Pair device with pairing code** and run the displayed values in PowerShell:

```powershell
adb pair PHONE_IP:PAIRING_PORT
adb connect PHONE_IP:CONNECTION_PORT
```

The pairing port and connection port may differ. Then click **Refresh devices** in DroidDesk. Use only a trusted network and disable wireless debugging when finished. For older Android versions, the workflow may differ.

## Use

- **Dashboard**: connection status, model, Android version, battery, storage.
- **Phone Control**: select a device and click **Start mirroring**. Mouse/keyboard control is provided by scrcpy.
- **Files**: browse shared storage, select a file, upload from PC or download to PC.
- **Apps**: refresh installed third-party packages and launch an app.
- **Settings**: set explicit paths to `adb.exe` and `scrcpy.exe`.

ADB commands are executed as argument lists (not through a shell). File paths are validated for the basic shared-storage workflow. Android may restrict protected app screens, some directories, or some actions. Do not expect this tool to bypass Android permissions.

## Build a Windows executable (optional)

```powershell
pip install pyinstaller
pyinstaller --noconfirm --clean --windowed --name DroidDesk main.py
```

This produces `dist\\DroidDesk\\` (or a one-file executable if you add `--onefile`). ADB and scrcpy are separate external dependencies unless you explicitly bundle and comply with their licenses.

## Troubleshooting

- **No devices**: check cable/data mode, USB driver, phone authorization and `adb devices`.
- **Unauthorized**: unlock the phone and accept the debugging prompt; reconnect if necessary.
- **ADB not found**: install Platform Tools or set the full `adb.exe` path in Settings.
- **Mirroring won't start**: install scrcpy, check `scrcpy --version`, and inspect the app output panel.
- **Wi-Fi device disappears**: wireless debugging may change ports or turn off; pair/connect again.
- **File operation fails**: use shared storage paths such as `/sdcard/Download`; Android may deny protected paths.
- **Battery/storage unavailable**: some Android vendors return different command output. Refresh the device information.

## Project structure

```text
DroidDesk/
├── main.py
├── requirements.txt
├── app/
│   ├── main_window.py
│   ├── theme.py
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── phone_control.py
│   │   ├── file_manager.py
│   │   ├── app_manager.py
│   │   └── settings.py
│   ├── services/
│   │   ├── adb_service.py
│   │   ├── device_service.py
│   │   ├── file_service.py
│   │   └── scrcpy_manager.py
│   └── database/
│       └── db_manager.py
├── tests/
└── data/
```
