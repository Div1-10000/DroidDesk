from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QStackedWidget, QMessageBox, QComboBox, QPlainTextEdit, QSplitter, QFileDialog
from PySide6.QtCore import Qt, QTimer
from .theme import APP_STYLE
from .services.adb_service import ADBService, ADBError
from .services.device_service import DeviceService
from .services.file_service import FileService
from .services.scrcpy_manager import ScrcpyManager
from .database.db_manager import DBManager
from .pages.dashboard import DashboardPage
from .pages.phone_control import PhoneControlPage
from .pages.file_manager import FileManagerPage
from .pages.app_manager import AppManagerPage
from .pages.settings import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DroidDesk — PC to Android Control Center")
        self.resize(1240, 800)
        self.db = DBManager()
        self.adb = ADBService(self.db.get_setting("adb_path"))
        self.device_service = DeviceService(self.adb)
        self.file_service = FileService(self.adb)
        self.scrcpy = ScrcpyManager(self.db.get_setting("scrcpy_path"))
        self.devices = []
        self.selected_serial = ""
        self.setStyleSheet(APP_STYLE)
        self._build_ui()
        self.refresh_devices()
        self.timer = QTimer(self); self.timer.timeout.connect(self.refresh_quietly); self.timer.start(12000)

    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        root = QHBoxLayout(central); root.setContentsMargins(14,14,14,14); root.setSpacing(14)
        sidebar = QFrame(); sidebar.setObjectName("Sidebar"); sidebar.setFixedWidth(218)
        side = QVBoxLayout(sidebar); side.setContentsMargins(12,16,12,14); side.setSpacing(7)
        brand = QLabel("◈  DroidDesk"); brand.setStyleSheet("font-size:18pt;font-weight:800;padding:8px;color:#ffffff;")
        side.addWidget(brand)
        tagline = QLabel("ANDROID CONTROL CENTER"); tagline.setObjectName("Muted"); tagline.setStyleSheet("font-size:8pt;padding:0 8px 10px;")
        side.addWidget(tagline)
        self.nav_buttons = []
        self.stack = QStackedWidget()
        self.dashboard = DashboardPage(self.refresh_devices)
        self.phone_page = PhoneControlPage(self.start_mirroring, self.stop_mirroring, self.navigation_action, self.take_screenshot)
        self.files_page = FileManagerPage(self.get_serial, self.file_service, self.notify)
        self.apps_page = AppManagerPage(self.get_serial, self.device_service, self.adb, self.notify)
        self.settings_page = SettingsPage(self.db, self.adb, self.scrcpy)
        pages = [
            ("⌂   Dashboard", self.dashboard),
            ("▣   Phone Control", self.phone_page),
            ("▤   File Manager", self.files_page),
            ("▦   Apps", self.apps_page),
            ("⚙   Settings", self.settings_page),
        ]
        for i, (label, page) in enumerate(pages):
            btn = QPushButton(label); btn.setObjectName("Nav"); btn.setCheckable(True)
            btn.clicked.connect(lambda checked=False, idx=i: self.show_page(idx))
            side.addWidget(btn); self.nav_buttons.append(btn); self.stack.addWidget(page)
        side.addStretch()
        self.device_combo = QComboBox(); self.device_combo.currentIndexChanged.connect(self.device_changed)
        side.addWidget(QLabel("ACTIVE DEVICE")); side.addWidget(self.device_combo)
        refresh_btn = QPushButton("↻  Refresh devices"); refresh_btn.clicked.connect(self.refresh_devices); side.addWidget(refresh_btn)
        self.status = QLabel("●  Initializing"); self.status.setObjectName("Muted"); side.addWidget(self.status)
        root.addWidget(sidebar)
        right = QVBoxLayout(); right.setSpacing(12)
        top = QHBoxLayout()
        self.top_title = QLabel("DroidDesk"); self.top_title.setStyleSheet("font-size:14pt;font-weight:700;")
        top.addWidget(self.top_title); top.addStretch()
        self.top_status = QLabel("No device"); self.top_status.setObjectName("Muted"); top.addWidget(self.top_status)
        right.addLayout(top)
        self.output = QPlainTextEdit(); self.output.setReadOnly(True); self.output.setMaximumBlockCount(250); self.output.setPlaceholderText("Activity and diagnostic output appears here.")
        self.output.setMaximumHeight(105)
        right.addWidget(self.stack, 1)
        output_frame = QFrame(); output_frame.setObjectName("Panel"); of = QVBoxLayout(output_frame); of.setContentsMargins(10,8,10,8)
        output_label = QLabel("ACTIVITY LOG"); output_label.setObjectName("Muted"); of.addWidget(output_label); of.addWidget(self.output)
        right.addWidget(output_frame)
        root.addLayout(right, 1)
        self.show_page(0)

    def show_page(self, index):
        self.stack.setCurrentIndex(index)
        for i, b in enumerate(self.nav_buttons): b.setChecked(i == index)
        self.top_title.setText(["Overview","Phone Control","File Manager","Apps","Settings"][index])

    def log(self, message, event_type="info"):
        self.output.appendPlainText(f"[{event_type.upper()}] {message}")
        try: self.db.log(event_type, message[:500])
        except Exception: pass

    def notify(self, message):
        self.log(str(message))
        self.statusBar().showMessage(str(message), 7000)

    def get_serial(self):
        return self.selected_serial or None

    def refresh_devices(self):
        current = self.selected_serial
        try:
            self.devices = self.adb.devices()
            self.device_combo.blockSignals(True); self.device_combo.clear()
            for d in self.devices:
                label = f"{d['serial']}  ·  {d['state']}"
                self.device_combo.addItem(label, d["serial"])
            idx = next((i for i,d in enumerate(self.devices) if d["serial"] == current), 0)
            if self.devices: self.device_combo.setCurrentIndex(idx)
            self.device_combo.blockSignals(False)
            self.selected_serial = self.device_combo.currentData() or ""
            if not self.devices:
                self.dashboard.set_info(None)
                self.status.setText("●  No device connected"); self.top_status.setText("No device")
                self.log("No ADB devices found. Connect USB or pair/connect through Wireless debugging.")
            else:
                d = self.devices[self.device_combo.currentIndex()]
                if d["state"] != "device":
                    self.dashboard.set_info(None)
                    self.status.setText(f"●  Device {d['state']}")
                    self.top_status.setText(d["state"])
                    self.log(f"Device {d['serial']} state is {d['state']}. Unlock and authorize the phone if needed.")
                else:
                    self.load_device_info()
        except Exception as exc:
            self.device_combo.blockSignals(False)
            self.dashboard.set_info(None)
            self.status.setText("●  ADB unavailable"); self.top_status.setText("Setup needed")
            self.log(str(exc), "error")

    def refresh_quietly(self):
        try:
            new = self.adb.devices()
            serials = [(x.get("serial"),x.get("state")) for x in new]
            old = [(x.get("serial"),x.get("state")) for x in self.devices]
            if serials != old: self.refresh_devices()
            elif self.selected_serial and any(x["serial"] == self.selected_serial and x["state"] == "device" for x in new):
                self.load_device_info(quiet=True)
        except Exception:
            pass

    def device_changed(self, index):
        serial = self.device_combo.itemData(index)
        if serial:
            self.selected_serial = serial
            self.load_device_info()

    def load_device_info(self, quiet=False):
        if not self.selected_serial: return
        try:
            device = next((d for d in self.devices if d["serial"] == self.selected_serial), {})
            if device.get("state") != "device":
                self.dashboard.set_info(None); return
            info = self.device_service.info(self.selected_serial)
            conn = "Wi-Fi" if ":" in self.selected_serial and not self.selected_serial.startswith("emulator-") else "USB / ADB"
            self.dashboard.set_info(info, conn)
            self.status.setText(f"●  Connected · {conn}"); self.top_status.setText(f"{info.get('battery')}% battery")
            if not quiet: self.log(f"Connected to {info.get('model')} ({self.selected_serial}).")
        except Exception as exc:
            if not quiet: self.log(f"Could not read device information: {exc}", "error")

    def start_mirroring(self):
        if not self.get_serial(): self.notify("Connect and select a device first."); return
        try:
            self.scrcpy.start(self.selected_serial); self.log("scrcpy mirroring launched.")
        except Exception as exc: self.notify(f"Could not start mirroring: {exc}")

    def stop_mirroring(self):
        self.scrcpy.stop(); self.log("scrcpy stop requested.")

    def navigation_action(self, action):
        serial = self.get_serial()
        if not serial: self.notify("Connect a device first."); return
        commands = {"home": ("input","keyevent","KEYCODE_HOME"),
                    "back": ("input","keyevent","KEYCODE_BACK"),
                    "recent": ("input","keyevent","KEYCODE_APP_SWITCH")}
        try:
            self.adb.shell(serial, *commands[action], timeout=10)
            self.log(f"Sent {action} navigation action.")
        except Exception as exc: self.notify(f"Navigation failed: {exc}")

    def take_screenshot(self):
        serial = self.get_serial()
        if not serial: self.notify("Connect a device first."); return
        path, _ = QFileDialog.getSaveFileName(self, "Save phone screenshot", "DroidDesk-screenshot.png", "PNG image (*.png)")
        if not path: return
        try:
            result = self.device_service.screenshot(serial, path)
            self.notify(result or f"Screenshot saved to {path}")
        except Exception as exc: self.notify(f"Screenshot failed: {exc}")

    def closeEvent(self, event):
        try: self.timer.stop()
        except Exception: pass
        self.scrcpy.stop()
        event.accept()
