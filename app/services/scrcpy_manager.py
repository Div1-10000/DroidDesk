import shutil
import subprocess
from pathlib import Path
from .adb_service import COMMON_SCRCPY_PATHS, ADBError

class ScrcpyManager:
    def __init__(self, scrcpy_path: str = ""):
        self.scrcpy_path = scrcpy_path.strip()
        self.process = None

    def executable(self):
        if self.scrcpy_path and Path(self.scrcpy_path).is_file():
            return self.scrcpy_path
        found = shutil.which("scrcpy")
        if found:
            return found
        for item in COMMON_SCRCPY_PATHS:
            if Path(item).is_file():
                return item
        raise ADBError("scrcpy was not found. Install scrcpy or set scrcpy.exe in Settings.")

    def start(self, serial: str):
        if self.process and self.process.poll() is None:
            return
        self.process = subprocess.Popen(
            [self.executable(), "--serial", serial],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            shell=False
        )

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=4)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.process = None

    def running(self):
        return self.process is not None and self.process.poll() is None
