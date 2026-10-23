import re
from .adb_service import ADBService

class DeviceService:
    def __init__(self, adb: ADBService):
        self.adb = adb

    def info(self, serial: str) -> dict:
        def prop(key):
            try:
                return self.adb.shell(serial, "getprop", key).strip() or "Unknown"
            except Exception:
                return "Unknown"
        model = prop("ro.product.manufacturer") + " " + prop("ro.product.model")
        android = prop("ro.build.version.release")
        sdk = prop("ro.build.version.sdk")
        try:
            battery_text = self.adb.shell(serial, "dumpsys", "battery")
            level_match = re.search(r"level:\s*(\d+)", battery_text)
            status_match = re.search(r"status:\s*(\d+)", battery_text)
            level = int(level_match.group(1)) if level_match else None
            status_code = int(status_match.group(1)) if status_match else 0
            status = {2: "Charging", 5: "Full", 3: "Discharging", 4: "Not charging"}.get(status_code, "Unknown")
        except Exception:
            level, status = None, "Unavailable"
        try:
            storage = self.adb.shell(serial, "df", "-h", "/sdcard")
            lines = storage.splitlines()
            storage_summary = " ".join(lines[-1].split()[:5]) if len(lines) > 1 else "Unavailable"
        except Exception:
            storage_summary = "Unavailable"
        try:
            uptime = self.adb.shell(serial, "uptime")
        except Exception:
            uptime = "Unavailable"
        return {
            "serial": serial, "model": model.strip(), "android": android,
            "sdk": sdk, "battery": level, "charging": status,
            "storage": storage_summary, "uptime": uptime
        }

    def packages(self, serial: str) -> list[str]:
        output = self.adb.shell(serial, "pm", "list", "packages", "-3")
        return sorted({line.replace("package:", "").strip() for line in output.splitlines() if line.startswith("package:")})

    def launch_package(self, serial: str, package: str) -> str:
        if not package or not re.fullmatch(r"[A-Za-z0-9_.]+", package):
            raise ValueError("Invalid package name.")
        return self.adb.shell(serial, "monkey", "-p", package, "-c",
                               "android.intent.category.LAUNCHER", "1", timeout=30)

    def screenshot(self, serial: str, local_path: str) -> str:
        import subprocess
        from pathlib import Path
        target = Path(local_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Use an argument list and a temporary remote path, then pull the screenshot.
        remote = "/sdcard/droiddesk_screenshot.png"
        self.adb.shell(serial, "screencap", "-p", remote, timeout=30)
        try:
            return self.adb.pull(serial, remote, str(target))
        finally:
            try:
                self.adb.shell(serial, "rm", "-f", remote)
            except Exception:
                pass
