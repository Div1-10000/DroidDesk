APP_STYLE = """
QWidget {
    background: #0a1020;
    color: #e8eefb;
    font-family: 'Segoe UI';
    font-size: 10pt;
}
QMainWindow { background: #080d19; }
QFrame#Sidebar {
    background: #0d1628;
    border: 1px solid #1e2b43;
    border-radius: 18px;
}
QFrame#Panel, QFrame#StatCard {
    background: #111c30;
    border: 1px solid #22324d;
    border-radius: 15px;
}
QFrame#StatCard:hover { border-color: #3b5d8b; background: #142139; }
QFrame#HeroPanel {
    background: #13223b;
    border: 1px solid #29456c;
    border-radius: 17px;
}
QLabel#PageTitle {
    font-size: 23pt;
    font-weight: 750;
    color: #f7f9ff;
}
QLabel#HeroTitle { font-size: 15pt; font-weight: 700; color: #f8fbff; }
QLabel#SectionTitle { font-size: 12pt; font-weight: 700; color: #f4f7ff; }
QLabel#Muted { color: #91a3bf; }
QLabel#CardLabel { color: #8ea2c0; font-size: 8pt; font-weight: 700; letter-spacing: 1px; }
QLabel#Metric { font-size: 19pt; font-weight: 750; color: #f7faff; }
QLabel#CardGlyph {
    background: #1b2d4a; color: #83b6ff; border-radius: 10px;
    font-size: 15pt; font-weight: 700;
}
QLabel#DeviceGlyph {
    background: #1b3b63; color: #8bc5ff; border-radius: 16px;
    font-size: 28pt; font-weight: 700;
}
QLabel#StatusBadge {
    background: #352817; color: #f5c879; border: 1px solid #594328;
    border-radius: 10px; padding: 8px 11px; font-size: 8pt; font-weight: 700;
}
QLabel#DetailText { color: #bdcbe0; line-height: 1.4; }
QPushButton {
    background: #1a2942; border: 1px solid #2b4162; border-radius: 9px;
    padding: 9px 13px; font-weight: 600; color: #e5edfb;
}
QPushButton:hover { background: #243a5c; border-color: #4f82c6; }
QPushButton:pressed { background: #14233b; }
QPushButton#Primary {
    background: #3478f6; border: 1px solid #4b8aff; color: white;
}
QPushButton#Primary:hover { background: #4b88ff; }
QPushButton#Nav {
    text-align: left; padding: 12px; background: transparent;
    border: 1px solid transparent; color: #b6c3d9;
}
QPushButton#Nav:checked, QPushButton#Nav:hover {
    background: #1a2a45; color: white; border-color: #263d60;
}
QLineEdit, QComboBox, QListWidget, QTreeWidget, QTextEdit, QPlainTextEdit {
    background: #0b1425; border: 1px solid #293954; border-radius: 8px;
    padding: 8px; selection-background-color: #3478f6;
}
QLineEdit:focus, QComboBox:focus, QTreeWidget:focus { border-color: #4b8aff; }
QHeaderView::section {
    background: #1a2840; color: #cdd8eb; padding: 8px; border: 0;
}
QProgressBar {
    background: #0a1322; border: 1px solid #283851; border-radius: 7px;
    text-align: center; min-height: 15px; color: #eaf2ff;
}
QProgressBar::chunk { background: #3478f6; border-radius: 5px; }
QScrollBar:vertical { background: #0b1425; width: 10px; margin: 0; }
QScrollBar::handle:vertical { background: #30415d; min-height: 25px; border-radius: 4px; }
QMessageBox { background: #121c30; }
"""
