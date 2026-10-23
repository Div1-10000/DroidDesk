from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QFileDialog, QMessageBox
class AppManagerPage(QWidget):
    def __init__(self, get_serial, device_service, adb, notify):
        super().__init__(); self.get_serial, self.device_service, self.adb, self.notify = get_serial, device_service, adb, notify
        layout = QVBoxLayout(self); layout.setContentsMargins(22,18,22,18); layout.setSpacing(12)
        title = QLabel("Apps"); title.setObjectName("PageTitle"); layout.addWidget(title)
        label = QLabel("List third-party packages, search, launch, or install an APK with your confirmation.")
        label.setObjectName("Muted"); layout.addWidget(label)
        row = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("Filter packages…"); self.search.textChanged.connect(self.filter)
        refresh = QPushButton("Refresh apps"); refresh.clicked.connect(self.refresh)
        launch = QPushButton("Launch selected"); launch.setObjectName("Primary"); launch.clicked.connect(self.launch)
        install = QPushButton("Install APK…"); install.clicked.connect(self.install)
        row.addWidget(self.search,1); row.addWidget(refresh); row.addWidget(launch); row.addWidget(install); layout.addLayout(row)
        self.list = QListWidget(); layout.addWidget(self.list,1); self.packages = []

    def filter(self, text):
        self.list.clear()
        self.list.addItems([p for p in self.packages if text.lower() in p.lower()])

    def refresh(self):
        serial = self.get_serial()
        if not serial: self.notify("Connect a device first."); return
        try:
            self.packages = self.device_service.packages(serial); self.filter(self.search.text())
            self.notify(f"Loaded {len(self.packages)} third-party packages.")
        except Exception as exc: self.notify(f"Could not list apps: {exc}")

    def launch(self):
        serial = self.get_serial(); item = self.list.currentItem()
        if not serial: self.notify("Connect a device first."); return
        if not item: self.notify("Select an app package."); return
        try: self.notify(self.device_service.launch_package(serial, item.text()) or "Launch command sent.")
        except Exception as exc: self.notify(f"Launch failed: {exc}")

    def install(self):
        serial = self.get_serial()
        if not serial: self.notify("Connect a device first."); return
        path, _ = QFileDialog.getOpenFileName(self, "Select APK", filter="Android packages (*.apk)")
        if not path: return
        confirm = QMessageBox.question(self, "Install APK", f"Install this APK on the connected phone?\n\n{path}")
        if confirm != QMessageBox.Yes: return
        try: self.notify(self.adb.install_app(serial, path) or "Installation complete.")
        except Exception as exc: self.notify(f"Install failed: {exc}")
