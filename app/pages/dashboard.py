from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar,
    QPushButton, QGridLayout
)
from PySide6.QtCore import Qt


def panel(object_name="Panel"):
    frame = QFrame()
    frame.setObjectName(object_name)
    return frame


class DashboardPage(QWidget):
    def __init__(self, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(18)

        header = QHBoxLayout()
        titles = QVBoxLayout()
        title = QLabel("Device overview")
        title.setObjectName("PageTitle")
        subtitle = QLabel("A clear view of your Android device and its live status.")
        subtitle.setObjectName("Muted")
        titles.addWidget(title)
        titles.addWidget(subtitle)
        header.addLayout(titles)
        header.addStretch()
        refresh = QPushButton("↻   Refresh")
        refresh.setObjectName("Primary")
        refresh.setMinimumHeight(40)
        refresh.clicked.connect(refresh_callback)
        header.addWidget(refresh)
        layout.addLayout(header)

        hero = panel("HeroPanel")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(22, 18, 22, 18)
        hero_layout.setSpacing(16)
        mark = QLabel("◈")
        mark.setObjectName("DeviceGlyph")
        mark.setAlignment(Qt.AlignCenter)
        mark.setFixedSize(62, 62)
        hero_layout.addWidget(mark)
        hero_text = QVBoxLayout()
        self.hero_title = QLabel("Ready when you are")
        self.hero_title.setObjectName("HeroTitle")
        self.hero_subtitle = QLabel("Connect a phone with USB debugging or wireless debugging enabled.")
        self.hero_subtitle.setObjectName("Muted")
        self.hero_subtitle.setWordWrap(True)
        hero_text.addWidget(self.hero_title)
        hero_text.addWidget(self.hero_subtitle)
        hero_layout.addLayout(hero_text, 1)
        self.connection_badge = QLabel("●  DISCONNECTED")
        self.connection_badge.setObjectName("StatusBadge")
        self.connection_badge.setAlignment(Qt.AlignCenter)
        hero_layout.addWidget(self.connection_badge, 0, Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(hero)

        self.cards = {}
        grid = QGridLayout()
        grid.setSpacing(14)
        specs = [
            ("connection", "CONNECTION", "Not connected", "↔", "Device link"),
            ("model", "DEVICE MODEL", "—", "▣", "Hardware"),
            ("android", "ANDROID VERSION", "—", "◉", "System"),
            ("battery", "BATTERY LEVEL", "—", "ϟ", "Power"),
        ]
        for idx, (key, label, value, glyph, hint) in enumerate(specs):
            card = panel("StatCard")
            box = QVBoxLayout(card)
            box.setContentsMargins(18, 16, 18, 17)
            top = QHBoxLayout()
            name = QLabel(label)
            name.setObjectName("CardLabel")
            symbol = QLabel(glyph)
            symbol.setObjectName("CardGlyph")
            symbol.setAlignment(Qt.AlignCenter)
            symbol.setFixedSize(34, 34)
            top.addWidget(name)
            top.addStretch()
            top.addWidget(symbol)
            box.addLayout(top)
            val = QLabel(value)
            val.setObjectName("Metric")
            val.setWordWrap(True)
            val.setMinimumHeight(36)
            box.addWidget(val)
            small = QLabel(hint)
            small.setObjectName("Muted")
            box.addWidget(small)
            self.cards[key] = val
            grid.addWidget(card, idx // 2, idx % 2)
        layout.addLayout(grid)

        lower = QHBoxLayout()
        lower.setSpacing(14)
        battery_panel = panel()
        bp = QVBoxLayout(battery_panel)
        bp.setContentsMargins(18, 17, 18, 18)
        battery_heading = QLabel("Power")
        battery_heading.setObjectName("SectionTitle")
        battery_caption = QLabel("Battery level reported by Android")
        battery_caption.setObjectName("Muted")
        bp.addWidget(battery_heading)
        bp.addWidget(battery_caption)
        self.battery_bar = QProgressBar()
        self.battery_bar.setRange(0, 100)
        self.battery_bar.setValue(0)
        self.battery_bar.setFormat("Waiting for device")
        self.battery_bar.setMinimumHeight(22)
        bp.addWidget(self.battery_bar)
        self.power_detail = QLabel("Charging status: —")
        self.power_detail.setObjectName("Muted")
        bp.addWidget(self.power_detail)
        lower.addWidget(battery_panel, 1)

        details_panel = panel()
        dp = QVBoxLayout(details_panel)
        dp.setContentsMargins(18, 17, 18, 18)
        heading = QLabel("Device details")
        heading.setObjectName("SectionTitle")
        dp.addWidget(heading)
        self.detail = QLabel("Connect your phone, approve the debugging prompt, then refresh devices.")
        self.detail.setObjectName("DetailText")
        self.detail.setWordWrap(True)
        self.detail.setTextInteractionFlags(Qt.TextSelectableByMouse)
        dp.addWidget(self.detail)
        lower.addWidget(details_panel, 1)
        layout.addLayout(lower)
        layout.addStretch()

    def set_info(self, info, connection_type=""):
        if not info:
            self.cards["connection"].setText("Not connected")
            self.cards["model"].setText("—")
            self.cards["android"].setText("—")
            self.cards["battery"].setText("—")
            self.hero_title.setText("Ready when you are")
            self.hero_subtitle.setText("Connect a phone with USB debugging or wireless debugging enabled.")
            self.connection_badge.setText("●  DISCONNECTED")
            self.connection_badge.setStyleSheet("")
            self.battery_bar.setValue(0)
            self.battery_bar.setFormat("Waiting for device")
            self.power_detail.setText("Charging status: —")
            self.detail.setText("No authorized device selected. Connect a phone and approve the debugging prompt.")
            return

        self.cards["connection"].setText(connection_type or "Connected")
        self.cards["model"].setText(info.get("model", "Unknown"))
        self.cards["android"].setText(f"Android {info.get('android', 'Unknown')}")
        level = info.get("battery")
        self.cards["battery"].setText(f"{level}%" if level is not None else "Unavailable")
        self.hero_title.setText(info.get("model", "Android device"))
        self.hero_subtitle.setText("Your device is connected and ready to manage.")
        self.connection_badge.setText("●  CONNECTED")
        self.connection_badge.setStyleSheet(
            "background:#123b32;color:#6ee7b7;border:1px solid #226b58;"
            "border-radius:10px;padding:8px 11px;font-size:8pt;font-weight:700;"
        )
        self.battery_bar.setValue(max(0, min(100, level or 0)))
        self.battery_bar.setFormat(f"{level}% battery" if level is not None else "Battery unavailable")
        self.power_detail.setText(f"Charging status: {info.get('charging', 'Unknown')}")
        self.detail.setText(
            f"Serial: {info.get('serial', '—')}\n"
            f"Android SDK: {info.get('sdk', '—')}\n"
            f"Shared storage: {info.get('storage', 'Unavailable')}\n"
            f"Uptime: {info.get('uptime', 'Unavailable')}"
        )
