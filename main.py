import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QDoubleSpinBox, QPushButton, 
                            QFrame, QStatusBar, QDialog, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QMetaObject, Q_ARG, pyqtSignal, pyqtSlot, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QColor, QLinearGradient, QPalette, QBrush
import pyautogui
from functools import partial
import keyboard

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About Modern Auto Clicker')
        self.setFixedSize(500, 400)  # Boyut artırıldı
        
        layout = QVBoxLayout()
        layout.setSpacing(30)  # Boşluk artırıldı
        layout.setContentsMargins(40, 40, 40, 40)  # Kenar boşlukları artırıldı
        
        title = QLabel('Modern Auto Clicker')
        title.setFont(QFont('Segoe UI', 20, QFont.Weight.Bold))  # Font boyutu artırıldı
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info = QLabel('''
        <h2>Developed by Hamza</h2>
        <p style='font-size: 14px;'>Version 1.0</p>
        <p style='font-size: 14px; margin: 20px 0;'>A modern, easy-to-use auto clicker with global hotkeys.</p>
        <p style='font-size: 14px;'>© 2024 All rights reserved.</p>
        ''')
        info.setTextFormat(Qt.TextFormat.RichText)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        close_btn.setFixedWidth(120)  # Genişlik artırıldı
        close_btn.setFixedHeight(40)  # Yükseklik artırıldı
        
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        self.setStyleSheet('''
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f0f0f0, stop:1 #e0e0e0);
                border-radius: 15px;
            }
            QLabel {
                color: #323130;
            }
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
        ''')

class ModernAutoClicker(QMainWindow):
    toggle_signal = pyqtSignal()
    close_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.click_timer = QTimer(self)
        self.click_timer.timeout.connect(self.perform_click)
        self.toggle_signal.connect(self.toggle)
        self.close_signal.connect(self.safe_close)
        self.initUI()
        keyboard.on_press_key('f6', lambda _: self.toggle_signal.emit())
        keyboard.on_press_key('esc', lambda _: self.close_signal.emit())

    def initUI(self):
        self.setWindowTitle('Modern Auto Clicker')
        self.setFixedSize(500, 400)  # Daha uygun bir boyut
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(40, 30, 40, 30)  # Kenarlardan daha fazla boşluk
        layout.setSpacing(20)
        
        # Başlık
        title = QLabel('Modern Auto Clicker')
        title.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setContentsMargins(0, 0, 0, 20)  # Başlık altında ekstra boşluk
        layout.addWidget(title)
        
        # Interval girişi için container
        interval_widget = QWidget()
        interval_layout = QHBoxLayout(interval_widget)
        interval_layout.setContentsMargins(0, 0, 0, 20)  # Alt kısımda ekstra boşluk
        
        interval_label = QLabel('Click Interval (seconds):')
        interval_label.setFont(QFont('Segoe UI', 12))
        interval_label.setFixedWidth(200)  # Sabit genişlik ile sola hizalama
        
        self.interval_input = QDoubleSpinBox()
        self.interval_input.setFont(QFont('Segoe UI', 12))
        self.interval_input.setDecimals(3)
        self.interval_input.setMinimum(0.001)
        self.interval_input.setMaximum(10.0)
        self.interval_input.setValue(0.1)
        self.interval_input.setSingleStep(0.1)
        self.interval_input.setFixedWidth(150)  # Input box'a sabit genişlik
        self.interval_input.setFixedHeight(35)
        
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_input)
        interval_layout.addStretch()  # Sağ tarafta boşluk bırakma
        layout.addWidget(interval_widget)
        
        # Start butonu
        self.toggle_button = QPushButton('Start (F6)')
        self.toggle_button.setFont(QFont('Segoe UI', 12))
        self.toggle_button.setFixedHeight(45)
        self.toggle_button.clicked.connect(self.toggle)
        layout.addWidget(self.toggle_button)
        
        # Ayırıcı çizgi
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("margin: 20px 0;")
        layout.addWidget(separator)
        
        # Shortcuts bölümü
        shortcuts_title = QLabel('Shortcuts')
        shortcuts_title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        shortcuts_title.setContentsMargins(0, 10, 0, 10)
        layout.addWidget(shortcuts_title)

        # Shortcuts listesi
        shortcuts_container = QWidget()
        shortcuts_layout = QVBoxLayout(shortcuts_container)
        shortcuts_layout.setContentsMargins(20, 0, 0, 0)  # Sol taraftan padding
        
        shortcuts = [
            'F6 - Start/Stop Clicking',
            'ESC - Exit Application'
        ]
        
        for shortcut in shortcuts:
            shortcut_label = QLabel(f"• {shortcut}")
            shortcut_label.setFont(QFont('Segoe UI', 12))
            shortcuts_layout.addWidget(shortcut_label)
        
        layout.addWidget(shortcuts_container)
        
        # About butonu için container
        bottom_container = QWidget()
        bottom_layout = QHBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 20, 0, 0)
        
        about_button = QPushButton('About')
        about_button.setFixedSize(100, 35)
        about_button.setFont(QFont('Segoe UI', 11))
        about_button.clicked.connect(self.show_about)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(about_button)
        layout.addWidget(bottom_container)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont('Segoe UI', 11))
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Ready')
        
        # Stil ayarları
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f8f8f8;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QDoubleSpinBox {
                padding: 5px 10px;
                border: 2px solid #0078D4;
                border-radius: 6px;
                background-color: white;
                color: black;
            }
            QStatusBar {
                background: #f0f0f0;
                color: #323130;
                min-height: 30px;
            }
        ''')
        
        self.center()

    # Diğer metodlar aynı kalacak
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    @pyqtSlot()
    def toggle(self):
        if not self.running:
            self.running = True
            interval = max(1, int(self.interval_input.value() * 1000))
            self.click_timer.start(interval)
            self.toggle_button.setText('Stop (F6)')
            self.toggle_button.setProperty('running', True)
            self.toggle_button.setStyle(self.toggle_button.style())
            self.statusBar.showMessage('Running')
        else:
            self.stop_clicking()

    def stop_clicking(self):
        self.running = False
        self.click_timer.stop()
        self.toggle_button.setText('Start (F6)')
        self.toggle_button.setProperty('running', False)
        self.toggle_button.setStyle(self.toggle_button.style())
        self.statusBar.showMessage('Stopped')

    @pyqtSlot()
    def safe_close(self):
        keyboard.unhook_all()
        self.stop_clicking()
        self.close()

    def closeEvent(self, event):
        keyboard.unhook_all()
        self.stop_clicking()
        event.accept()
            
    def perform_click(self):
        pyautogui.click()

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

def main():
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ModernAutoClicker()
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())