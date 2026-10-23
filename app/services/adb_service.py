from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

COMMON_ADB_PATHS = [
    r"C:\platform-tools\adb.exe",
    r"C:\Android\platform-tools\adb.exe",
    str(Path.home() / "AppData/Local/Android/Sdk/platform-tools/adb.exe"),
]
COMMON_SCRCPY_PATHS = [
    r"C:\scrcpy\scrcpy.exe",
    r"C:\Program Files\scrcpy\scrcpy.exe",
    str(Path.home() / "scoop/apps/scrcpy/current/scrcpy.exe"),
]

class ADBError(RuntimeError):
    pass

class ADBService:
    def __init__(self, adb_path: str = "", timeout: int = 15):
        self.adb_path = adb_path.strip()
        self.timeout = timeout

    def executable(self) -> str:
        candidate = self.adb_path
        if candidate and Path(candidate).is_file():
            return candidate
        found = shutil.which("adb")
        if found:
            return found
        for item in COMMON_ADB_PATHS:
            if Path(item).is_file():
                return item
        raise ADBError("ADB was not found. Install Android Platform Tools or set adb.exe in Settings.")

    def run(self, *args: str, serial: Optional[str] = None, timeout: Optional[int] = None) -> str:
        cmd = [self.executable()]
        if serial:
            cmd += ["-s", serial]
        cmd.extend(str(a) for a in args)
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=timeout or self.timeout, shell=False
            )
        except subprocess.TimeoutExpired as exc:
            raise ADBError(f"ADB command timed out after {exc.timeout}s.") from exc
        except OSError as exc:
            raise ADBError(f"Could not run ADB: {exc}") from exc
        output = (result.stdout or "").strip()
        error = (result.stderr or "").strip()
        if result.returncode != 0:
            raise ADBError(error or output or f"ADB exited with code {result.returncode}.")
        return output

    def devices(self) -> list[dict[str, str]]:
        output = self.run("devices", "-l")
        rows = []
        for line in output.splitlines()[1:]:
            line = line.strip()
            if not line or line.startswith("*"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            serial, state = parts[0], parts[1]
            details = {}
            for item in parts[2:]:
                if ":" in item:
                    k, v = item.split(":", 1)
                    details[k] = v
            rows.append({"serial": serial, "state": state, **details})
        return rows

    def shell(self, serial: str, *args: str, timeout: Optional[int] = None) -> str:
        return self.run("shell", *args, serial=serial, timeout=timeout)

    def push(self, serial: str, local_path: str, remote_path: str) -> str:
        if not Path(local_path).is_file():
            raise ADBError("Select an existing local file.")
        return self.run("push", str(Path(local_path)), remote_path, serial=serial, timeout=180)

    def pull(self, serial: str, remote_path: str, local_path: str) -> str:
        target = Path(local_path)
        if target.exists() and target.is_dir():
            pass
        elif target.parent and not target.parent.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
        return self.run("pull", remote_path, str(target), serial=serial, timeout=180)

    def install_app(self, serial: str, apk_path: str) -> str:
        if not Path(apk_path).is_file() or Path(apk_path).suffix.lower() != ".apk":
            raise ADBError("Select a valid APK file.")
        return self.run("install", "-r", apk_path, serial=serial, timeout=180)
