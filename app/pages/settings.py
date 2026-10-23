from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QFrame
class SettingsPage(QWidget):
    def __init__(self, db, adb, scrcpy):
        super().__init__(); self.db, self.adb, self.scrcpy = db, adb, scrcpy
        layout = QVBoxLayout(self); layout.setContentsMargins(22,18,22,18); layout.setSpacing(14)
        title = QLabel("Settings"); title.setObjectName("PageTitle"); layout.addWidget(title)
        panel = QFrame(); panel.setObjectName("Panel"); box = QVBoxLayout(panel); box.setContentsMargins(18,18,18,18)
        box.addWidget(QLabel("Tool paths (leave blank to use PATH or common install locations)"))
        self.adb_edit = QLineEdit(db.get_setting("adb_path")); self.adb_edit.setPlaceholderText("Path to adb.exe")
        self.scrcpy_edit = QLineEdit(db.get_setting("scrcpy_path")); self.scrcpy_edit.setPlaceholderText("Path to scrcpy.exe")
        for label, edit, key in [("ADB executable", self.adb_edit, "adb_path"), ("scrcpy executable", self.scrcpy_edit, "scrcpy_path")]:
            row = QHBoxLayout(); row.addWidget(QLabel(label)); row.addWidget(edit,1)
            browse = QPushButton("Browse…"); browse.clicked.connect(lambda checked=False, e=edit: self.browse(e))
            row.addWidget(browse); box.addLayout(row)
        save = QPushButton("Save settings"); save.setObjectName("Primary"); save.clicked.connect(self.save)
        box.addWidget(save); layout.addWidget(panel)
        note = QLabel("DroidDesk uses Android's authorized debugging interface. Keep USB/Wireless debugging disabled when not needed, and only pair trusted computers.")
        note.setObjectName("Muted"); note.setWordWrap(True); layout.addWidget(note); layout.addStretch()

    def browse(self, edit):
        path, _ = QFileDialog.getOpenFileName(self, "Select executable", filter="Executable (*.exe)")
        if path: edit.setText(path)

    def save(self):
        self.db.set_setting("adb_path", self.adb_edit.text().strip())
        self.db.set_setting("scrcpy_path", self.scrcpy_edit.text().strip())
        self.adb.adb_path = self.adb_edit.text().strip()
        self.scrcpy.scrcpy_path = self.scrcpy_edit.text().strip()
        self.adb_changed = True
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Settings saved", "Tool paths saved. Refresh devices if the ADB path changed.")
