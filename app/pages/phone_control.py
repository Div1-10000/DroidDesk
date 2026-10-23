from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
class PhoneControlPage(QWidget):
    def __init__(self, start_cb, stop_cb, action_cb, screenshot_cb):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(22,18,22,18); layout.setSpacing(14)
        title = QLabel("Phone Control"); title.setObjectName("PageTitle"); layout.addWidget(title)
        intro = QLabel("Launch scrcpy to mirror and control the real Android screen. The mirrored screen opens in its own window.")
        intro.setObjectName("Muted"); intro.setWordWrap(True); layout.addWidget(intro)
        panel = QFrame(); panel.setObjectName("Panel"); box = QVBoxLayout(panel); box.setContentsMargins(18,18,18,18)
        box.addWidget(QLabel("Screen mirroring"))
        row = QHBoxLayout()
        start = QPushButton("▶  Start mirroring"); start.setObjectName("Primary"); start.clicked.connect(start_cb)
        stop = QPushButton("■  Stop mirroring"); stop.clicked.connect(stop_cb)
        row.addWidget(start); row.addWidget(stop); row.addStretch(); box.addLayout(row)
        box.addWidget(QLabel("Navigation controls (availability depends on Android version and device policy)"))
        nav = QHBoxLayout()
        for label, action in [("Home","home"),("Back","back"),("Overview","recent")]:
            btn = QPushButton(label); btn.clicked.connect(lambda checked=False, a=action: action_cb(a)); nav.addWidget(btn)
        shot = QPushButton("Take screenshot"); shot.clicked.connect(screenshot_cb); nav.addWidget(shot); nav.addStretch()
        box.addLayout(nav); layout.addWidget(panel)
        note = QLabel("Tip: scrcpy supports mouse clicks, typing, scrolling and device navigation. Keep the phone unlocked for initial authorization.")
        note.setObjectName("Muted"); note.setWordWrap(True); layout.addWidget(note); layout.addStretch()
