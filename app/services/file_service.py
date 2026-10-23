from pathlib import PurePosixPath, PurePath
from .adb_service import ADBService

def normalize_remote_path(path: str) -> str:
    path = (path or "/sdcard").strip()
    if "\\x00" in path:
        raise ValueError("Invalid path.")
    if ".." in path.split("/"):
        raise ValueError("Parent-directory segments are not allowed.")
    if not path.startswith("/"):
        path = "/sdcard/" + path
    normalized = str(PurePosixPath(path))
    if normalized == "/" or not (normalized == "/sdcard" or normalized.startswith("/sdcard/")):
        raise ValueError("For safety, DroidDesk file browsing is limited to shared storage under /sdcard.")
    return normalized

class FileService:
    def __init__(self, adb: ADBService):
        self.adb = adb

    def list_dir(self, serial: str, remote_path: str) -> list[dict]:
        path = normalize_remote_path(remote_path)
        output = self.adb.shell(serial, "ls", "-la", path, timeout=30)
        entries = []
        for line in output.splitlines():
            parts = line.split(None, 7)
            if len(parts) < 8 or line.startswith("total "):
                continue
            name = parts[7]
            if name in (".", ".."):
                continue
            entries.append({"name": name, "details": " ".join(parts[:5]), "directory": parts[0].startswith("d")})
        return entries

    def push(self, serial: str, local_path: str, remote_dir: str) -> str:
        remote_dir = normalize_remote_path(remote_dir)
        name = __import__("pathlib").Path(local_path).name
        if not name or name in (".", ".."):
            raise ValueError("Invalid local filename.")
        return self.adb.push(serial, local_path, remote_dir.rstrip("/") + "/" + name)

    def pull(self, serial: str, remote_path: str, local_path: str) -> str:
        return self.adb.pull(serial, normalize_remote_path(remote_path), local_path)
