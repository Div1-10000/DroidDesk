from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTreeWidget, QTreeWidgetItem, QFileDialog, QMessageBox, QInputDialog
from PySide6.QtCore import Qt
from pathlib import PurePosixPath

class FileManagerPage(QWidget):
    def __init__(self, get_serial, file_service, notify):
        super().__init__()
        self.get_serial, self.file_service, self.notify = get_serial, file_service, notify
        self.current_path = "/sdcard"
        layout = QVBoxLayout(self); layout.setContentsMargins(22,18,22,18); layout.setSpacing(12)
        title = QLabel("File Manager"); title.setObjectName("PageTitle"); layout.addWidget(title)
        info = QLabel("Browse shared storage under /sdcard. Android may restrict some directories.")
        info.setObjectName("Muted"); layout.addWidget(info)
        row = QHBoxLayout()
        self.path = QLineEdit(self.current_path); self.path.setPlaceholderText("/sdcard/Download")
        go = QPushButton("Open path"); go.clicked.connect(self.load_path)
        up = QPushButton("↑ Parent"); up.clicked.connect(self.parent_dir)
        row.addWidget(self.path, 1); row.addWidget(go); row.addWidget(up); layout.addLayout(row)
        self.tree = QTreeWidget(); self.tree.setHeaderLabels(["Name", "Type", "Details"]); self.tree.itemDoubleClicked.connect(self.open_item)
        layout.addWidget(self.tree, 1)
        actions = QHBoxLayout()
        refresh = QPushButton("Refresh"); refresh.clicked.connect(self.load_path)
        upload = QPushButton("Upload from PC"); upload.setObjectName("Primary"); upload.clicked.connect(self.upload)
        download = QPushButton("Download selected"); download.clicked.connect(self.download)
        actions.addWidget(refresh); actions.addWidget(upload); actions.addWidget(download); actions.addStretch(); layout.addLayout(actions)

    def load_path(self):
        serial = self.get_serial()
        if not serial: self.notify("Connect a device first."); return
        try:
            self.current_path = self.path.text().strip() or "/sdcard"
            entries = self.file_service.list_dir(serial, self.current_path)
            self.tree.clear()
            for e in entries:
                item = QTreeWidgetItem([e["name"], "Folder" if e["directory"] else "File", e["details"]])
                item.setData(0, Qt.UserRole, e)
                self.tree.addTopLevelItem(item)
            self.path.setText(self.current_path)
        except Exception as exc: self.notify(f"Could not browse folder: {exc}")

    def parent_dir(self):
        p = PurePosixPath(self.current_path)
        if str(p) not in ("/", "/sdcard"):
            self.path.setText(str(p.parent)); self.load_path()

    def open_item(self, item, column):
        e = item.data(0, Qt.UserRole)
        if e and e["directory"]:
            self.path.setText(self.current_path.rstrip("/") + "/" + e["name"]); self.load_path()

    def upload(self):
        serial = self.get_serial()
        if not serial: self.notify("Connect a device first."); return
        local, _ = QFileDialog.getOpenFileName(self, "Choose file to upload")
        if not local: return
        try:
            result = self.file_service.push(serial, local, self.current_path)
            self.notify(result or "Upload complete."); self.load_path()
        except Exception as exc: self.notify(f"Upload failed: {exc}")

    def download(self):
        serial = self.get_serial()
        if not serial: self.notify("Connect a device first."); return
        item = self.tree.currentItem()
        if not item: self.notify("Select a file first."); return
        e = item.data(0, Qt.UserRole)
        if not e or e["directory"]: self.notify("Select a file, not a folder."); return
        remote = self.current_path.rstrip("/") + "/" + e["name"]
        local, _ = QFileDialog.getSaveFileName(self, "Save downloaded file", e["name"])
        if not local: return
        try:
            result = self.file_service.pull(serial, remote, local)
            self.notify(result or "Download complete.")
        except Exception as exc: self.notify(f"Download failed: {exc}")
