from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QStackedWidget, QFrame, QLabel

from qfluentwidgets import FluentIcon
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor)
from qframelesswindow import FramelessWindow, StandardTitleBar

from interface.chat_gpt import ChatGpt


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))
        self.clicked = False


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.h_box_layout = QHBoxLayout(self)
        self.navigation_interface = NavigationInterface(self, showMenuButton=True)
        self.stack_widget = QStackedWidget(self)
        self.chat_gpt_interface = ChatGpt(self)

        self.setTitleBar(StandardTitleBar(self))
        self.init_window()
        self.set_qss()
        self.init_layout()
        self.init_navigation()

    def init_window(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('./interface/resource/logo.png'))
        self.setWindowTitle('Sphinx')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def init_layout(self):
        self.h_box_layout.setSpacing(0)
        self.h_box_layout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.h_box_layout.addWidget(self.navigation_interface)
        self.h_box_layout.addWidget(self.stack_widget)
        self.h_box_layout.setStretchFactor(self.stack_widget, 1)

    def set_qss(self):
        with open(f'./interface/resource/light/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def add_sub_interface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        self.stack_widget.addWidget(interface)
        self.navigation_interface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            position=position,
            tooltip=text,
            onClick=lambda: self.nave_switch(interface)
        )

    def init_navigation(self):
        self.add_sub_interface(self.chat_gpt_interface, FluentIcon.CHAT, 'ChatGPT')

    def nave_switch(self, widget):
        self.stack_widget.setCurrentWidget(widget)
